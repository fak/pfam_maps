from django.template import Context, loader, RequestContext
from pfam_maps.models import PfamMaps, ValidDomains
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.core.servers.basehttp import FileWrapper
import os
from django.db import connection
import itertools
import helper
import time
from django.contrib.auth import authenticate, login, logout
import csv


def index(request):
    """
    Return the ppdms start page.
    """
    return render_to_response('pfam_maps/index.html', context_instance=RequestContext(request))

def evidence_portal(request):
    """
    Return the evidence portal page showing a summary of all pfam_a domains
    with evidence for small molecule bining.
    """
    data = helper.custom_sql('SELECT DISTINCT domain_name FROM pfam_maps', [])
    names = sorted([x[0] for x in data])
    held_doms = helper.custom_sql("""
    SELECT DISTINCT domain_name, comment, timestamp, submitter
    FROM held_domains
    """, [])
    c = Context({
        'names': names,
        'held_doms' : held_doms
        })
    return render_to_response('pfam_maps/evidence_portal.html',c, context_instance=RequestContext(request))


def evidence(request, pfam_name):
    """
    Return the evidence page for individual Pfam-A domains. To improve
    load times, only process the first 1500 query results.
    """
    dois = ValidDomains.objects.filter(domain_name=pfam_name)
    cits = []
    for doi in dois:
        cits.append(helper.doi2json(doi.evidence))
    acts = helper.custom_sql("""
    SELECT DISTINCT act.standard_value, act.standard_units, act.standard_type, act.activity_id, act.molregno, single_domains.accession
    FROM pfam_maps pm
        JOIN activities act
            ON act.activity_id = pm.activity_id
        JOIN assays ass
            ON act.assay_id = ass.assay_id
        JOIN target_dictionary td
            ON ass.tid = td.tid
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
        WHERE domain_name = %s
        AND standard_relation= '='
        AND assay_type = 'B'
        AND relationship_type = 'D'
        AND td.target_type IN('SINGLE PROTEIN')
        LIMIT 1500
        """ , [pfam_name])
    (std_acts, lkp) = helper.standardize_acts(acts)
    (top_mols, top_acts) = helper.filter_acts(std_acts, lkp)
    n_acts = len(std_acts)
    c = Context({
        'top_mols'  : top_mols,
        'top_acts'  : top_acts,
        'pfam_name' : pfam_name,
        'n_acts'    : n_acts,
        'cits'      : cits,
        })
    return render_to_response('pfam_maps/evidence.html',c, context_instance=RequestContext(request))

def conflict_portal(request):
    """
    Return a summary of all conflicting architectures and provide some summary
    stats.
    """
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
    c = Context({
        'act_count'   : act_count,
        'man_count'   : man_count,
        'dub_count'   : dub_count,
        'clash_count' : clash_count,
        'clash_arch'  : clash_arch,
        })
    return render_to_response('pfam_maps/conflict_portal.html',c, context_instance=RequestContext(request))

def resolved_portal(request):
    """
    Return a summary of all conflicting architectures and provide some
    summary stats.
    """
    clash_arch = helper.custom_sql("""
    SELECT DISTINCT activity_id, domain_name FROM pfam_maps WHERE category_flag=2 AND manual_flag=1""", [])
    clash_arch = helper.process_arch(clash_arch)
    clash_acts = (list(itertools.chain(*clash_arch.values())))
    c = Context({
        'clash_count' : len(clash_acts),
        'clash_arch'  : clash_arch,
        })
    return render_to_response('pfam_maps/resolved_portal.html',c, context_instance=RequestContext(request))


def vote_on_assay(request, conflict_id, assay_id):
    """
    Commit changes specified in html form to database and return the next
    conflict view, or start page, if n/a.
    """
    if not request.user.is_authenticated():
        return render_to_response('pfam_maps/user_portal.html',context_instance=RequestContext(request))
    try:
        domain_name = request.POST['choice']
    except KeyError:
        return HttpResponseRedirect(reverse('conflicts', args=(conflict_id,)))
    try:
        comment = request.POST['comment']
    except KeyError:
        comment = "committed w/o comment"
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
            entry.submitter = request.user.get_username()
            entry.timestamp = time.strftime('%d %B %Y %T', time.gmtime())
            if entry.compd_id == compd_id:
                entry.status_flag = 0
            entry.save()
    return HttpResponseRedirect(reverse('conflicts', args=(conflict_id,)))

def revoke_assay(request, conflict_id, assay_id):
    """
    Commit a revoke instruction to the database, return next conflict or start
    site, if n/a.
    """
    if not request.user.is_authenticated():
        return render_to_response('pfam_maps/user_portal.html',context_instance=RequestContext(request))
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
            entry.submitter = request.user.get_username()
            entry.save()
    return HttpResponseRedirect(reverse('resolved', args=(conflict_id,)))



def conflicts(request, conflict_id):
    """
    Return page for individual assay. Show assay_id, description, pubmed_id,
    assay target, edit time and domain structure.
    """
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
        assays = clash_arch[conflict_id]
    except KeyError:
        return render_to_response('pfam_maps/index.html',context_instance=RequestContext(request))
    paginator = Paginator(assays, 1)
    page = int(request.GET.get('page', '1'))
    try:
        page_idx = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_idx = paginator.page(paginator.num_pages)
    assay_id = page_idx.object_list[0]
    assay_page = helper.get_assay_meta(assay_id)
    assay_page = helper.get_pfam_arch(assay_page)
    dom_l = conflict_id.split(' vs. ')
    c = {
         'ass'          : assay_id,
         'arch'         : conflict_id,
         'assay_page'   : assay_page,
         'doms'         : dom_l,
         'page_idx'     : page_idx,
        }
    return render_to_response('pfam_maps/conflict.html',c, context_instance=RequestContext(request))


def resolved(request, conflict_id):
    """
    Return page for individual assay. Show assay_id, description, pubmed_id,
    assay target, edit time and domain structure.
    """
    doms = conflict_id.split(' vs. ')
    placeholder = "%s"
    placeholder = ','.join([placeholder] * len(doms))
    query = """
    SELECT DISTINCT pm.domain_name, ass.chembl_id, pm.status_flag
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
    mapped_doms = helper.mapped_dom(data)
    clash_arch = helper.arch_assays(data)
    try:
        assays = clash_arch[conflict_id]
    except KeyError:
        return render_to_response('pfam_maps/index.html',context_instance=RequestContext(request))
    paginator = Paginator(assays, 1)
    page = int(request.GET.get('page', '1'))
    try:
        page_idx = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_idx = paginator.page(paginator.num_pages)
    assay_id = page_idx.object_list[0]
    mapped_dom = mapped_doms[assay_id]
    assay_page = helper.get_assay_meta(assay_id)
    assay_page = helper.get_pfam_arch(assay_page)
    dom_l = conflict_id.split(' vs. ')
    c = {
         'mapped_dom'   : mapped_dom,
         'ass'          : assay_id,
         'arch'         : conflict_id,
         'assay_page'   : assay_page,
         'doms'         : dom_l,
         'page_idx'     : page_idx,
        }
    return render_to_response('pfam_maps/resolved.html',c, context_instance=RequestContext(request))


def user_portal(request):
    """
    Return the user_portal template.
    """
    return render_to_response('pfam_maps/user_portal.html', context_instance=RequestContext(request))


def about(request):
    """
    Return the About template.
    """
    n_total = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id)
    FROM activities act
    JOIN assays ass
      ON ass.assay_id = act.assay_id
    JOIN target_dictionary td
      ON ass.tid = td.tid
    WHERE act.pchembl_value IS NOT NULL
    AND ass.assay_type IN('B', 'F')
    AND td.target_type IN('PROTEIN COMPLEX', 'SINGLE PROTEIN')
    AND ass.relationship_type = 'D'
    """, [])[0][0]
    n_mapped = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps
    """, [])[0][0]
    n_straight = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps
    WHERE category_flag = 0
    """, [])[0][0]
    n_ambigs = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps
    WHERE category_flag = 1
    """, [])[0][0]
    n_confl = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps
    WHERE category_flag = 2
            """, [])[0][0]
    n_res = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id) FROM pfam_maps
    WHERE manual_flag = 1
    """, [])[0][0]
    chembl_version = helper.custom_sql("""
    SELECT name FROM version
    """, [])[0][0]
    n_none = n_total - n_mapped
    n_confl_comb = n_confl + n_ambigs
    n_unres = n_confl - n_res
    n_none = n_total - n_mapped
    n_confl_comb = n_confl + n_ambigs
    n_unres = n_confl - n_res
    c = Context({
        'n_total'   : helper.perc(n_total, n_total),
        'n_none'    : helper.perc(n_none, n_total),
        'n_mapped'  : helper.perc(n_mapped, n_total),
        'n_straight': helper.perc(n_straight, n_total),
        'n_ambigs'  : helper.perc(n_ambigs, n_confl_comb),
        'n_confl'   : helper.perc(n_confl, n_total),
        'n_confl_comb': helper.perc(n_confl_comb, n_total),
        'n_res'     : helper.perc(n_res, n_confl_comb),
        'n_unres'   : helper.perc(n_unres, n_confl_comb),
        'chembl_version' : chembl_version
        })
    return render_to_response('pfam_maps/about.html', c, context_instance=RequestContext(request))


def alt_about(request):
    """
    Return an alternative About template that summarises ACTIVE activities.
    This takes a lot longer to query and is therefore inactive by default. If
    you want to use it, switch view names about <-> alternative_about.
    """
    n_total = helper.custom_sql("""
    SELECT COUNT(DISTINCT activity_id)
    FROM activities act
    JOIN assays ass
      ON ass.assay_id = act.assay_id
    JOIN target_dictionary td
      ON ass.tid = td.tid
    WHERE act.pchembl_value IS NOT NULL
    AND ass.assay_type IN('B','F')
    AND td.target_type IN('PROTEIN COMPLEX', 'SINGLE PROTEIN')
    AND ass.relationship_type = 'D'
    AND act.pchembl_value > 5
    """, [])[0][0]
    n_mapped = helper.custom_sql("""
    SELECT COUNT(DISTINCT pm.activity_id)
    FROM pfam_maps pm
    JOIN activities act
    ON pm.activity_id = act.activity_id
    JOIN assays ass
      ON ass.assay_id = act.assay_id
    WHERE ass.assay_type IN('B', 'F')
    AND act.pchembl_value > 5
    """, [])[0][0]
    n_straight = helper.custom_sql("""
    SELECT COUNT(DISTINCT pm.activity_id)
    FROM pfam_maps pm
    JOIN activities act
    ON pm.activity_id = act.activity_id
    JOIN assays ass
      ON ass.assay_id = act.assay_id
    WHERE ass.assay_type IN('B', 'F')
    AND category_flag = 0
    AND act.pchembl_value > 5
    """, [])[0][0]
    n_ambigs = helper.custom_sql("""
    SELECT COUNT(DISTINCT pm.activity_id)
    FROM pfam_maps pm
    JOIN activities act
    ON pm.activity_id = act.activity_id
    JOIN assays ass
      ON ass.assay_id = act.assay_id
    WHERE ass.assay_type IN('B', 'F')
    AND category_flag = 1
    AND act.pchembl_value > 5
    """, [])[0][0]
    n_confl = helper.custom_sql("""
    SELECT COUNT(DISTINCT pm.activity_id)
    FROM pfam_maps pm
    JOIN activities act
    ON pm.activity_id = act.activity_id
    JOIN assays ass
      ON ass.assay_id = act.assay_id
    WHERE ass.assay_type IN('B','F')
    AND category_flag = 2
    AND act.pchembl_value > 5
            """, [])[0][0]
    n_res = helper.custom_sql("""
    SELECT COUNT(DISTINCT pm.activity_id)
    FROM pfam_maps pm
    JOIN activities act
    ON pm.activity_id = act.activity_id
    JOIN assays ass
      ON ass.assay_id = act.assay_id
    WHERE ass.assay_type IN('B','F')
    AND manual_flag = 1
    AND act.pchembl_value > 5
    """, [])[0][0]
    n_none = n_total - n_mapped
    n_confl_comb = n_confl + n_ambigs
    n_unres = n_confl - n_res
    c = Context({
        'n_total'   : helper.perc(n_total, n_total),
        'n_none'    : helper.perc(n_none, n_total),
        'n_mapped'  : helper.perc(n_mapped, n_total),
        'n_straight': helper.perc(n_straight, n_total),
        'n_ambigs'  : helper.perc(n_ambigs, n_confl_comb),
        'n_confl'   : helper.perc(n_confl, n_total),
        'n_confl_comb': helper.perc(n_confl_comb, n_total),
        'n_res'     : helper.perc(n_res, n_confl_comb),
        'n_unres'   : helper.perc(n_unres, n_confl_comb),
        })
    return render_to_response('pfam_maps/about.html', c, context_instance=RequestContext(request))


def logout_view(request):
    """
    Log out user and return to the user_portal view.
    """
    logout(request)
    return HttpResponseRedirect('../profile/')

def login_view(request):
    """
    Log in user and return to the user_portal view.
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    c={}
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to success pagei.
            return render_to_response('pfam_maps/user_portal.html',c,context_instance=RequestContext(request))
        else:
            # Return a 'disabled account' error message
            return render_to_response('pfam_maps/user_portal.html',c, context_instance=RequestContext(request))
    else:
        # Return an 'invalid login' error message.
            return render_to_response('pfam_maps/user_portal.html',c, context_instance=RequestContext(request))

def logs_portal(request):
    """
    Show a log of manual asignments ordered by timestamp. Include a search field to identify assignments
    based on user name or comment string.
    """
    query = """SELECT timestamp, submitter, assay_id
               FROM pfam_maps pm
               JOIN activities act 
                ON pm.activity_id = act.activity_id
               WHERE manual_flag = 1"""
    logs_raw = helper.custom_sql(query, [])
    logs = []
    lkp = {}
    for log in logs_raw:
        assay_id = log[2]
        try:
            lkp[assay_id]
        except KeyError:
            lkp[assay_id] = True
            logs.append(log)
    #logs_t = [(time.strptime(tt[0],'%d %B %Y %H:%M:%S'), tt[1]) for tt in logs]
    logs = sorted(logs, key=lambda x: x[0], reverse=True)
    #logs = [(time.strftime('%d %B %Y %H:%M:%S', tt[0]), tt[1]) for tt in logs_t]
    paginator = Paginator(logs, 50)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        log_idx = paginator.page(page)
    except (EmptyPage, InvalidPage):
        log_idx = paginator.page(paginator.num_pages)
    c = {
         'log_idx'  : log_idx,
        }
    return render_to_response('pfam_maps/logs_portal.html',c, context_instance=RequestContext(request))

def logs(request):
    """
    Return page for individual assay. Show assay_id, description, pubmed_id,
    assay target, edit time and domain structure.
    """
    assay_id  = request.GET.get('assay_id','')
    query = """
    SELECT DISTINCT pm.domain_name, ass.chembl_id, pm.status_flag
        FROM pfam_maps pm
        JOIN activities act
          ON act.activity_id = pm.activity_id
        JOIN assays ass
          ON act.assay_id = ass.assay_id
          WHERE manual_flag = 1
          AND category_flag = 2
          AND act.assay_id = %s
        """ % assay_id
    data = helper.custom_sql(query, [])
    mapped_doms = helper.mapped_dom(data)
    clash_arch = helper.arch_assays(data)
    assays = {}
    for arch in clash_arch:
        for ass_id in clash_arch[arch]:
            assays[ass_id] = arch
    paginator = Paginator(assays.keys(), 1)
    page = int(request.GET.get('page', '1'))
    try:
        page_idx = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_idx = paginator.page(paginator.num_pages)
    assay_id = page_idx.object_list[0]
    mapped_dom = mapped_doms[assay_id]
    assay_page = helper.get_assay_meta(assay_id)
    assay_page = helper.get_pfam_arch(assay_page)
    conflict_id = assays[assay_id]
    dom_l = conflict_id.split(' vs. ')
    c = {
         'mapped_dom'   : mapped_dom,
         'ass'          : assay_id,
         'arch'         : conflict_id,
         'assay_page'   : assay_page,
         'doms'         : dom_l,
         'page_idx'     : page_idx,
        }
    return render_to_response('pfam_maps/logs.html',c, context_instance=RequestContext(request))


def query_logs(request):
    """
    Query the pfam_maps table for query terms provided by the user and return the entries.
    """
    try:
        request.session['submitter'] = request.POST['submitter']
        request.session['comment']=request.POST['comment']
    except KeyError:
        pass
    query = """
    SELECT DISTINCT pm.domain_name, ass.chembl_id
        FROM pfam_maps pm
        JOIN activities act
          ON act.activity_id = pm.activity_id
        JOIN assays ass
          ON act.assay_id = ass.assay_id
          WHERE manual_flag = 1
          AND category_flag = 2
          AND submitter ~ %s
          AND comment ~ %s
        """
    data = helper.custom_sql(query, [request.session['submitter'], request.session['comment']])
    clash_arch = helper.arch_assays(data)
    assays = {}
    for arch in clash_arch.keys():
        for ass_id in clash_arch[arch]:
            assays[ass_id] = arch
    paginator = Paginator(assays.keys(), 1)
    page = int(request.GET.get('page', '1'))
    try:
        page_idx = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_idx = paginator.page(paginator.num_pages)
    assay_id = page_idx.object_list[0]
    assay_page = helper.get_assay_meta(assay_id)
    assay_page = helper.get_pfam_arch(assay_page)
    conflict_id = assays[assay_id]
    dom_l = conflict_id.split(' vs. ')
    c = {
         'ass'          : assay_id,
         'arch'         : conflict_id,
         'assay_page'   : assay_page,
         'doms'         : dom_l,
         'arch_idx'     : page_idx,
        }
    return render_to_response('pfam_maps/query_logs.html',c, context_instance=RequestContext(request))


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def download_logs(request):
    qres = helper.custom_sql("""SELECT * FROM pfam_maps WHERE NOT submitter = 'system'""", [])
    #qres=PfamMaps.objects.all.iterator()
    pseudo_buffer=Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in qres),content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pfam_maps.csv'
    return response


def download_pfam(request):
    qres = helper.custom_sql("""SELECT * FROM valid_domains""", [])
    pseudo_buffer=Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in qres),content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=valid_domains.txt'
    return response


