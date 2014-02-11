from django.template import Context, loader, RequestContext
from pfam_maps.models import PfamMaps
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.db import connection
import itertools
import helper
import time
from django.contrib.auth import authenticate, login


def index(request):
    t = loader.get_template('pfam_maps/index.html')
    c = Context({
        })
    return HttpResponse(t.render(c))


def evidence_portal(request):
    data = helper.custom_sql('SELECT DISTINCT domain_name FROM pfam_maps', [])
    names = sorted([x[0] for x in data])
    t = loader.get_template('pfam_maps/evidence_portal_ebi.html')
    c = Context({
        'names': names,
    })
    return HttpResponse(t.render(c))


def evidence(request, pfam_name):
    acts = helper.custom_sql("""
    SELECT DISTINCT act.standard_value, act.standard_units, act.standard_type, act.activity_id, act.molregno, single_domains.accession
    FROM pfam_maps pm
        JOIN activities act
            ON act.activity_id = pm.activity_id
        JOIN assays ass
            ON act.assay_id = ass.assay_id
        JOIN (SELECT  tid, cs.accession
                FROM component_domains cd
                    JOIN component_sequences cs
                        ON cd.component_id = cs.component_id
                    JOIN target_components tc
                        ON tc.component_id = cs.component_id
                    GROUP BY tid, cs.accession
                    HAVING COUNT(compd_id) =1)
        AS single_domains
        ON single_domains.tid = ass.tid
        WHERE domain_name = %s AND standard_relation= '=' AND assay_type = 'B' AND relationship_type = 'D' LIMIT 1500
        """ , [pfam_name])
    (std_acts, lkp) = helper.standardize_acts(acts)
    (top_mols, top_acts) = helper.filter_acts(std_acts, lkp)
    t = loader.get_template('pfam_maps/evidence_ebi.html')
    n_acts = len(std_acts)
    c = Context({
        'top_mols'  : top_mols,
        'top_acts'  : top_acts,
        'pfam_name' : pfam_name,
        'n_acts'    : n_acts
        })
    return HttpResponse(t.render(c))


def conflicts_portal(request):
    act_count = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps WHERE category_flag = 0
    """, [])[0][0]
    dub_count = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps WHERE category_flag = 1
    """, [])[0][0]
    man_count = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps WHERE manual_flag = 1
    """, [])[0][0]
    clash_count = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps WHERE category_flag = 2
            """, [])[0][0]
    clash_arch = helper.custom_sql("""
    SELECT DISTINCT activity_id, domain_name FROM pfam_maps WHERE category_flag=2 AND manual_flag=0""", [])
    clash_arch = helper.process_arch(clash_arch)
    # Uncomment in case we want list the number of assays rather than activities.
    #data = helper.custom_sql("""
    #SELECT DISTINCT pm.domain_name, ass.chembl_id
    #    FROM pfam_maps pm
    #    JOIN activities act
    #      ON act.activity_id = pm.activity_id
    #    JOIN assays ass
    #      ON act.assay_id = ass.assay_id
    #    WHERE pm.status_flag = 1
    #      AND manual_flag = 0
    #      AND category_flag = 2
    #    """, [])
    #clash_arch = helper.arch_assays(data)
    t = loader.get_template('pfam_maps/conflict_portal_ebi.html')
    c = Context({
        'act_count'   : act_count,
        'man_count'   : man_count,
        'dub_count'   : dub_count,
        'clash_count' : clash_count,
        'clash_arch'  : clash_arch,
        })
    return HttpResponse(t.render(c))

def resolved_portal(request):
    clash_arch = helper.custom_sql("""
    SELECT DISTINCT activity_id, domain_name FROM pfam_maps WHERE category_flag=2 AND manual_flag=1""", [])
    clash_arch = helper.process_arch(clash_arch)
    clash_acts = (list(itertools.chain(*clash_arch.values())))
    t = loader.get_template('pfam_maps/resolved_portal_ebi.html')
    c = Context({
        'clash_count' : len(clash_acts),
        'clash_arch'  : clash_arch,
        })
    return HttpResponse(t.render(c))

def vote_on_activity(request, conflict_id, act):
    try:
        domain_name = request.POST['choice']
    except KeyError:
        return render_to_response('index.html', {
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    data = helper.custom_sql("""
    SELECT DISTINCT compd_id
        FROM pfam_maps
        WHERE activity_id = %s AND domain_name = %s
        """ ,[act, domain_name])[0]
    for compd_id in data:
        new_entry = PfamMaps(activity_id= act, compd_id = compd_id, domain_name = domain_name, status_flag = 0, manual_flag = 1 )
        new_entry.save()
    return HttpResponseRedirect(reverse('conflicts', args=(conflict_id,)))


def vote_on_assay(request, conflict_id, assay_id):
    try:
        domain_name = request.POST['choice']
    except KeyError:
        return HttpResponseRedirect(reverse('conflicts', args=(conflict_id,)))
    try:
        comment = request.POST['comment']
    except KeyError:
        comment = "revoked w/o comment"
    data = helper.custom_sql("""
    SELECT DISTINCT act.activity_id, compd_id
        FROM pfam_maps pm
        JOIN activities act
          ON act.activity_id = pm.activity_id
        JOIN assays ass
          ON ass.assay_id = act.assay_id
        WHERE ass.chembl_id = %s AND domain_name = %s
        """ ,[assay_id, domain_name])
    for ent in data:
        act = ent[0]
        compd_id = ent[1]
        entries = PfamMaps.objects.filter(activity_id=act)
        for entry in entries:
            entry.manual_flag = 1
            entry.comment = comment
            entry.timestamp = time.strftime('%d %B %Y %T', time.gmtime())
            if entry.compd_id == compd_id:
                entry.status_flag = 0
            entry.save()
    return HttpResponseRedirect(reverse('conflicts', args=(conflict_id,)))


def revoke_assay(request, conflict_id, assay_id):
    try:
        comment = request.POST['comment']
    except KeyError:
        comment = "revoked w/o comment"
    data = helper.custom_sql("""
    SELECT DISTINCT act.activity_id
        FROM pfam_maps pm
        JOIN activities act
          ON act.activity_id = pm.activity_id
        JOIN assays ass
          ON ass.assay_id = act.assay_id
        WHERE ass.chembl_id = %s
        """ ,[assay_id])
    for ent in data:
        act = ent[0]
        entries = PfamMaps.objects.filter(activity_id=act)
        for entry in entries:
            entry.manual_flag = 0
            entry.status_flag = 1
            entry.comment = comment
            entry.timestamp = time.strftime('%d %B %Y %T', time.gmtime())
            entry.save()
    return HttpResponseRedirect(reverse('resolved', args=(conflict_id,)))



def conflicts(request, conflict_id):
    doms = conflict_id.split(' vs. ')
    placeholder = "%s"
    placeholder = ','.join([placeholder] * len(doms))
    query = """
    SELECT DISTINCT pm.domain_name, ass.chembl_id
        FROM pfam_maps pm
        JOIN activities act
          ON act.activity_id = pm.activity_id
        JOIN assays ass
          ON act.assay_id = ass.assay_id
        WHERE pm.status_flag = 1
          AND manual_flag = 0
          AND category_flag = 2
          AND domain_name IN(%s)
        """ % placeholder
    data = helper.custom_sql(query, doms)
    clash_arch = helper.arch_assays(data)
    try:
        arch_assays = clash_arch[conflict_id]
        #out = open('test.txt','w')
        #for ass in arch_assays:
        #    out.write(ass + "', '")
        #out.close()
    except KeyError:
        return render_to_response('pfam_maps/index.html')
    assay_hier = {}
    for ass_id in arch_assays:
        assay_hier[ass_id] = {}
    paginator = Paginator(assay_hier.keys(), 1)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        arch_idx = paginator.page(page)
    except (EmptyPage, InvalidPage):
        arch_idx = paginator.page(paginator.num_pages)
    assay_hier_page = dict((k, assay_hier[k]) for k in arch_idx.object_list)
    assay_hier_page = helper.get_assay_meta(assay_hier_page)
    assay_hier_page = helper.get_pfam_arch(assay_hier_page)
    dom_l = conflict_id.split(' vs. ')
    c = {'arch'         : conflict_id,
         'assay_hier'   : assay_hier_page,
         'doms'         : dom_l,
         'arch_idx'     : arch_idx
        }
    return render_to_response('pfam_maps/conflict_ebi.html',c, context_instance=RequestContext(request))


def resolved(request, conflict_id):
    doms = conflict_id.split(' vs. ')
    placeholder = "%s"
    placeholder = ','.join([placeholder] * len(doms))
    query = """
    SELECT DISTINCT pm.domain_name, ass.chembl_id
        FROM pfam_maps pm
        JOIN activities act
          ON act.activity_id = pm.activity_id
        JOIN assays ass
          ON act.assay_id = ass.assay_id
          WHERE manual_flag = 1
          AND category_flag = 2
          AND domain_name IN(%s)
        """ % placeholder
    data = helper.custom_sql(query, doms)
    clash_arch = helper.arch_assays(data)
    try:
        arch_assays = clash_arch[conflict_id]
    except KeyError:
        return render_to_response('pfam_maps/index.html')
    assay_hier = {}
    for ass_id in arch_assays:
        assay_hier[ass_id] = {}
    paginator = Paginator(assay_hier.keys(), 1)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        arch_idx = paginator.page(page)
    except (EmptyPage, InvalidPage):
        arch_idx = paginator.page(paginator.num_pages)
    assay_hier_page = dict((k, assay_hier[k]) for k in arch_idx.object_list)
    assay_hier_page = helper.get_assay_meta(assay_hier_page)
    assay_hier_page = helper.get_pfam_arch(assay_hier_page)
    dom_l = conflict_id.split(' vs. ')
    c = {'arch'         : conflict_id,
         'assay_hier'   : assay_hier_page,
         'doms'         : dom_l,
         'arch_idx'     : arch_idx
        }
    return render_to_response('pfam_maps/resolved_ebi.html',c, context_instance=RequestContext(request))


def details(request, assay_id):
    data = helper.custom_sql("""
    SELECT DISTINCT act.molregno, md.chembl_id,  ass.chembl_id, ass.description
        FROM activities act
        JOIN assays ass
          ON ass.assay_id = act.assay_id
        JOIN molecule_dictionary md
          ON md.molregno = act.molregno
        WHERE assay_id = %s
        """, [act])
    mols = {}
    for ent in data:
        molregno = data[0]
        m_chembl = data[1]
        mols[molregno] = m_chembl
    a_chembl = data[2]
    desc = data[3]
    c = {'mols'     : mols,
         'ass_id'   : ass_id,
         'desc'     : desc,
        }
    return render_to_response('pfam_maps/details_ebi.html',c,                          context_instance=RequestContext(request))


def login_launch(request):
    c = {
        }
    return render_to_response('registration/login.html',c, context_instance=RequestContext(request))


def logout(request):
    c = {
        }
    return render_to_response('registration/login.html',c, context_instance=RequestContext(request))


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    c={}
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to success page.
            return render_to_response('pfam_maps/index.html',c,context_instance=RequestContext(request))
        else:
            # Return a 'disabled account' error message 
            return render_to_response('pfam_maps/index.html',c,context_instance=RequestContext(request))
    else:
        # Return an 'invalid login' error message.
        print 'bah'
