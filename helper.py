from django.db import connection
import numpy as np
import yaml
import simplejson as json
from operator import itemgetter
import requests

def custom_sql(query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    return data



def get_assay_meta(assay_page):
    assay_1 = assay_page.keys()[0]
    try:
        assay_2 = assay_page.keys()[1]
    except IndexError:
        assay_2 = 'This string is not a foreign key in the assays table'
    metas = custom_sql("""
    SELECT DISTINCT ass.chembl_id, dcs.pubmed_id, cs.accession, td.pref_name,
            ass.description
        FROM activities act
        JOIN docs dcs
          ON act.doc_id = dcs.doc_id
        JOIN assays ass
          ON ass.assay_id = act.assay_id
        JOIN target_dictionary td
          ON td.tid = ass.tid
        JOIN target_components tc
          ON tc.tid = td.tid
        JOIN component_sequences cs
          ON tc.component_id = cs.component_id
        WHERE ass.chembl_id IN (%s, %s)
        """, [assay_1, assay_2 ])
    component_d = {}
    pref_name_d = {}
    pubmed_d = {}
    for meta in metas:
        assay_id =  str(meta[0])
        pubmed_id =  meta[1]
        uniprot = meta[2]
        pref_name = meta[3]
        description = meta[4]
        try:
            assay_page[assay_id]['components'].append(uniprot)
        except KeyError:
            assay_page[assay_id]['components'] =  [uniprot]
            assay_page[assay_id]['pref_name']= pref_name
            assay_page[assay_id]['pubmed'] =  pubmed_id
            assay_page[assay_id]['description'] = description
    metas = custom_sql("""
    SELECT ass.chembl_id, pm.comment, pm.timestamp
        FROM activities act
        JOIN assays ass
          ON ass.assay_id = act.assay_id
        JOIN pfam_maps pm
          ON pm.activity_id = act.activity_id
        WHERE ass.chembl_id IN (%s, %s) LIMIT 1
        """, [assay_1, assay_2 ])
    assay_id = metas[0][0]
    assay_page[assay_id]['comment'] = metas[0][1]
    assay_page[assay_id]['timestamp'] = metas[0][2]
    return assay_page


def get_pfam_arch(assay_page):
    for ass in assay_page.keys():
        for uniprot in assay_page[ass]['components']:
            r = requests.get('http://pfam.sanger.ac.uk/protein/%s/graphic'% uniprot)
            doms = r.content
            #doms = '[{"length":"950","regions":[{"colour":"#2dcf00", "endStyle":"jagged","end":"361","startStyle":"jagged","text":"Peptidase_S8","href":"/family/PF00082","type":"pfama","start": "159"},]}]' #this would be an example of a pfam-architecture obtained in this way.
            try:
                assay_page[ass]['pfam_archs'].append(doms)
            except KeyError:
                assay_page[ass]['pfam_archs']=[doms]
    return assay_page


def standardize_acts(acts):
    paramFile = open('local.yaml')
    params = yaml.safe_load(paramFile)
    ki_adjust = params['ki_adjust']
    std_acts = []
    lkp = {}
    for data in acts:
        try:
            standard_value = float(data[0])
        except TypeError:
            continue
        pass_filter = False # set filter
        standard_units = data[1]
        standard_type = data[2]
        act_id = data[3]
        molregno = data[4]
        accession = data[5]
        # p-scaling.
        if standard_type in ['Ki','Kd','IC50','EC50', 'AC50'] and standard_units == 'nM':
            standard_value = -(np.log10(standard_value)-9)
            standard_type = 'p' + standard_type
            pass_filter = True
        # p-scaling.
        if standard_type in ['log Ki', 'log Kd', 'log IC50', 'log EC50', 'logAC50'] and standard_units is None:
            standard_value = - standard_value
            standard_type = 'p' + standard_type.split(' ')[1]
            pass_filter = True
        # Mixing types.
        if standard_type in ['pKi', 'pKd']:
            standard_value = standard_value - ki_adjust
            pass_filter = True
        # Filtering inactives.
        if standard_value >= 3 and pass_filter:
            std_acts.append((molregno, standard_value, accession, act_id))
            try:
                lkp[molregno] += 1
            except KeyError:
                lkp[molregno] = 1
    return (std_acts, lkp)

def add_meta(top_acts):
    act_ids = [str(x[3]) for x in top_acts]
    act_str = "','".join(act_ids)
    data = custom_sql("""SELECT act.activity_id, td.pref_name, ass.chembl_id, td.chembl_id, md.chembl_id
                                 FROM activities act
                                 JOIN assays ass
                                     ON act.assay_id = ass.assay_id
                                 JOIN target_dictionary td
                                     ON ass.tid = td.tid
                                 JOIN molecule_dictionary md
                                     ON md.molregno = act.molregno
                                 WHERE activity_id IN('%s')""" % act_str, [])
    lkp = {}
    for meta in data:
        act = meta[0]
        lkp[act] = (meta[1], meta[2], meta[3], meta[4])
    top_acts = [x + lkp[x[3]]  for x in top_acts]
    return top_acts

def filter_acts(std_acts, lkp):
    top_mols = [key for key,value in sorted(lkp.items(), key=itemgetter(1), reverse = True)][:10]
    top_acts = [x for x in std_acts if x[0] in top_mols]
    top_acts = add_meta(top_acts)
    top_mols = json.dumps(top_mols)
    top_acts = json.dumps(top_acts)
    return(top_mols, top_acts)

def process_arch(data):
    lkp = {}
    for clash in data:
        act_id = clash[0]
        dom = str(clash[1])
        try:
            lkp[act_id] = ' vs. '.join(sorted([lkp[act_id], dom]))
        except KeyError:
            lkp[act_id] = dom
    inv_lkp = dictinvert(lkp)
    return inv_lkp

def arch_assays(data):
    lkp = {}
    for clash in data:
        assay_id = clash[1]
        dom = clash[0]
        try:
            lkp[assay_id] = ' vs. '.join(sorted([lkp[assay_id], dom]))
        except KeyError:
            lkp[assay_id] = dom
    inv_lkp = dictinvert(lkp)
    return inv_lkp


def dictinvert(d):
        inv = {}
        for k, v in d.iteritems():
            try:
                inv[v].append(k)
            except KeyError:
                inv[v] = [k]
        return inv


def group_acts(arch_assays, data):
    assay_hier = {}
    for clash in data:
        assay_id = clash[1]
        if assay_id in arch_assays and not assay_id in assay_hier.keys():
             description = clash[2]
             assay_hier[assay_id] = {'description':description}
    return assay_hier

def count_votes(dom_l, arch_acts):
    domstr = "','".join(dom_l)
    counts = custom_sql("""
    SELECT activity_id, domain_name
        FROM pfam_maps
        WHERE manual_flag = 1 AND domain_name IN('%s')
        """%domstr, [])
    doms = {}
    for act in arch_acts:
        doms[act]={}
        for dom in domL:
            doms[act][dom]=0
    for ent in counts:
        dom = ent[1]
        act = ent[0]
        try:
            doms[act][dom] +=1
        except KeyError:
            pass
    return doms




# Currently not in use.
#def get_arch(data):
#    trc = []
#    #[(domain_name, start, end), ...]
#    for ent in data:
#
#        domain_name = ent[6]
#        start = ent[4]
#        end = ent[5]
#        trc.append((domain_name, start, end))
#    return trc


#def process_acts(arch_acts, data):
#    arch_mols = {}
#    for clash in data:
#        act_id = clash[0]
#        if act_id in arch_acts:
#             molregno = clash[2]
#             try:
#                 arch_mols[molregno][act_id]=0
#             except KeyError:
#                 arch_mols[molregno] = {act_id:0}
#    return arch_mols



