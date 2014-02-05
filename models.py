# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class ActionType(models.Model):
    action_type = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=200)
    parent_type = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'action_type'

class Activities(models.Model):
    activity_id = models.BigIntegerField(primary_key=True)
    assay = models.ForeignKey('Assays')
    doc = models.ForeignKey('Docs', null=True, blank=True)
    record = models.ForeignKey('CompoundRecords')
    molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='molregno', blank=True)
    standard_relation = models.CharField(max_length=50, blank=True)
    published_value = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    published_units = models.CharField(max_length=100, blank=True)
    standard_value = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    standard_units = models.CharField(max_length=100, blank=True)
    standard_flag = models.SmallIntegerField(null=True, blank=True)
    standard_type = models.CharField(max_length=250, blank=True)
    activity_comment = models.CharField(max_length=4000, blank=True)
    published_type = models.CharField(max_length=250, blank=True)
    data_validity_comment = models.ForeignKey('DataValidityLookup', null=True, db_column='data_validity_comment', blank=True)
    potential_duplicate = models.SmallIntegerField(null=True, blank=True)
    published_relation = models.CharField(max_length=50, blank=True)
    pchembl_value = models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)
    class Meta:
        db_table = 'activities'

class ActivityStdsLookup(models.Model):
    std_act_id = models.IntegerField(primary_key=True)
    standard_type = models.CharField(max_length=250)
    definition = models.CharField(max_length=500, blank=True)
    standard_units = models.CharField(max_length=100)
    normal_range_min = models.DecimalField(null=True, max_digits=24, decimal_places=12, blank=True)
    normal_range_max = models.DecimalField(null=True, max_digits=24, decimal_places=12, blank=True)
    class Meta:
        db_table = 'activity_stds_lookup'

class AssayType(models.Model):
    assay_type = models.CharField(max_length=1, primary_key=True)
    assay_desc = models.CharField(max_length=250, blank=True)
    class Meta:
        db_table = 'assay_type'

class Assays(models.Model):
    assay_id = models.IntegerField(primary_key=True)
    doc = models.ForeignKey('Docs')
    description = models.CharField(max_length=4000, blank=True)
    assay_type = models.ForeignKey(AssayType, null=True, db_column='assay_type', blank=True)
    assay_test_type = models.CharField(max_length=20, blank=True)
    assay_category = models.CharField(max_length=20, blank=True)
    assay_organism = models.CharField(max_length=250, blank=True)
    assay_tax_id = models.BigIntegerField(null=True, blank=True)
    assay_strain = models.CharField(max_length=200, blank=True)
    assay_tissue = models.CharField(max_length=100, blank=True)
    assay_cell_type = models.CharField(max_length=100, blank=True)
    assay_subcellular_fraction = models.CharField(max_length=100, blank=True)
    tid = models.ForeignKey('TargetDictionary', null=True, db_column='tid', blank=True)
    relationship_type = models.ForeignKey('RelationshipType', null=True, db_column='relationship_type', blank=True)
    confidence_score = models.ForeignKey('ConfidenceScoreLookup', null=True, db_column='confidence_score', blank=True)
    curated_by = models.ForeignKey('CurationLookup', null=True, db_column='curated_by', blank=True)
    src = models.ForeignKey('Source')
    src_assay_id = models.CharField(max_length=50, blank=True)
    chembl = models.ForeignKey('ChemblIdLookup', unique=True)
    class Meta:
        db_table = 'assays'

class AsscascComponents(models.Model):
    accession = models.CharField(max_length=-1, blank=True)
    saez_id = models.CharField(max_length=-1, blank=True)
    class Meta:
        db_table = 'asscasc_components'

class AsscascDocs(models.Model):
    doc_id = models.IntegerField(null=True, blank=True)
    assay_id = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    tid = models.IntegerField(null=True, blank=True)
    assay_type = models.CharField(max_length=-1, blank=True)
    class Meta:
        db_table = 'asscasc_docs'

class AsscascFassays(models.Model):
    assay_id = models.IntegerField(primary_key=True)
    doc_id = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=-1, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    assay_type = models.CharField(max_length=-1, blank=True)
    system_label = models.CharField(max_length=-1, blank=True)
    functional_label = models.CharField(max_length=-1, blank=True)
    timestamp = models.CharField(max_length=-1, blank=True)
    comment = models.CharField(max_length=-1, blank=True)
    curator = models.CharField(max_length=-1, blank=True)
    class Meta:
        db_table = 'asscasc_fassays'

class AsscascRawDocs(models.Model):
    doc_id = models.IntegerField(null=True, blank=True)
    assay_id = models.IntegerField(null=True, blank=True)
    assay_type = models.CharField(max_length=1, blank=True)
    count = models.BigIntegerField(null=True, blank=True)
    tid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'asscasc_raw_docs'

class AsscascTargets(models.Model):
    saez_id = models.CharField(max_length=-1, blank=True)
    tid = models.IntegerField(null=True, blank=True)
    target_type = models.CharField(max_length=-1, blank=True)
    class Meta:
        db_table = 'asscasc_targets'

class AtcClassification(models.Model):
    who_name = models.CharField(max_length=150, blank=True)
    level1 = models.CharField(max_length=10, blank=True)
    level2 = models.CharField(max_length=10, blank=True)
    level3 = models.CharField(max_length=10, blank=True)
    level4 = models.CharField(max_length=10, blank=True)
    level5 = models.CharField(max_length=10, primary_key=True)
    who_id = models.CharField(max_length=15, blank=True)
    level1_description = models.CharField(max_length=150, blank=True)
    level2_description = models.CharField(max_length=150, blank=True)
    level3_description = models.CharField(max_length=150, blank=True)
    level4_description = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = 'atc_classification'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class BindingSites(models.Model):
    site_id = models.IntegerField(primary_key=True)
    site_name = models.CharField(max_length=200, blank=True)
    tid = models.ForeignKey('TargetDictionary', null=True, db_column='tid', blank=True)
    class Meta:
        db_table = 'binding_sites'

class BioComponentSequences(models.Model):
    component_id = models.IntegerField(primary_key=True)
    component_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    sequence = models.TextField(blank=True)
    sequence_md5sum = models.CharField(max_length=32, blank=True)
    tax_id = models.BigIntegerField(null=True, blank=True)
    organism = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = 'bio_component_sequences'

class BiotherapeuticComponents(models.Model):
    biocomp_id = models.IntegerField(primary_key=True)
    molregno = models.ForeignKey('Biotherapeutics', db_column='molregno')
    component = models.ForeignKey(BioComponentSequences)
    class Meta:
        db_table = 'biotherapeutic_components'

class Biotherapeutics(models.Model):
    molregno = models.ForeignKey('MoleculeDictionary', primary_key=True, db_column='molregno')
    description = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = 'biotherapeutics'

class CellDictionary(models.Model):
    cell_id = models.IntegerField(primary_key=True)
    cell_name = models.CharField(max_length=50)
    cell_description = models.CharField(max_length=200, blank=True)
    cell_source_tissue = models.CharField(max_length=50, blank=True)
    cell_source_organism = models.CharField(max_length=150, blank=True)
    cell_source_tax_id = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'cell_dictionary'

class ChemblIdLookup(models.Model):
    chembl_id = models.CharField(max_length=20, primary_key=True)
    entity_type = models.CharField(max_length=50, blank=True)
    entity_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'chembl_id_lookup'

class ComponentClass(models.Model):
    component = models.ForeignKey('ComponentSequences')
    protein_class = models.ForeignKey('ProteinClassification')
    comp_class_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'component_class'

class ComponentDomains(models.Model):
    compd_id = models.IntegerField(primary_key=True)
    domain = models.ForeignKey('Domains', null=True, blank=True)
    component = models.ForeignKey('ComponentSequences')
    start_position = models.IntegerField(null=True, blank=True)
    end_position = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'component_domains'

class ComponentSequences(models.Model):
    component_id = models.IntegerField(primary_key=True)
    component_type = models.CharField(max_length=50, blank=True)
    accession = models.CharField(max_length=25, unique=True, blank=True)
    sequence = models.TextField(blank=True)
    sequence_md5sum = models.CharField(max_length=32, blank=True)
    description = models.CharField(max_length=200, blank=True)
    tax_id = models.BigIntegerField(null=True, blank=True)
    organism = models.CharField(max_length=150, blank=True)
    db_source = models.CharField(max_length=25, blank=True)
    db_version = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'component_sequences'

class ComponentSynonyms(models.Model):
    compsyn_id = models.IntegerField(primary_key=True)
    component = models.ForeignKey(ComponentSequences)
    component_synonym = models.CharField(max_length=500, blank=True)
    syn_type = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = 'component_synonyms'

class CompoundProperties(models.Model):
    molregno = models.ForeignKey('MoleculeDictionary', primary_key=True, db_column='molregno')
    mw_freebase = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    alogp = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    hba = models.SmallIntegerField(null=True, blank=True)
    hbd = models.SmallIntegerField(null=True, blank=True)
    psa = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    rtb = models.SmallIntegerField(null=True, blank=True)
    ro3_pass = models.CharField(max_length=3, blank=True)
    num_ro5_violations = models.SmallIntegerField(null=True, blank=True)
    med_chem_friendly = models.CharField(max_length=3, blank=True)
    acd_most_apka = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    acd_most_bpka = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    acd_logp = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    acd_logd = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    molecular_species = models.CharField(max_length=50, blank=True)
    full_mwt = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    aromatic_rings = models.SmallIntegerField(null=True, blank=True)
    heavy_atoms = models.SmallIntegerField(null=True, blank=True)
    num_alerts = models.SmallIntegerField(null=True, blank=True)
    qed_weighted = models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True)
    updated_on = models.DateField(null=True, blank=True)
    mw_monoisotopic = models.DecimalField(null=True, max_digits=11, decimal_places=4, blank=True)
    full_molformula = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'compound_properties'

class CompoundRecords(models.Model):
    record_id = models.IntegerField(primary_key=True)
    molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='molregno', blank=True)
    doc = models.ForeignKey('Docs')
    compound_key = models.CharField(max_length=250, blank=True)
    compound_name = models.CharField(max_length=4000, blank=True)
    src = models.ForeignKey('Source')
    src_compound_id = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'compound_records'

class CompoundStructures(models.Model):
    molregno = models.ForeignKey('MoleculeDictionary', primary_key=True, db_column='molregno')
    molfile = models.TextField(blank=True)
    standard_inchi = models.CharField(max_length=4000, blank=True)
    standard_inchi_key = models.CharField(max_length=27, unique=True)
    canonical_smiles = models.CharField(max_length=4000, blank=True)
    class Meta:
        db_table = 'compound_structures'

class ConfidenceScoreLookup(models.Model):
    confidence_score = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    target_mapping = models.CharField(max_length=30)
    class Meta:
        db_table = 'confidence_score_lookup'

class CurationLookup(models.Model):
    curated_by = models.CharField(max_length=32, primary_key=True)
    description = models.CharField(max_length=100)
    class Meta:
        db_table = 'curation_lookup'

class DataValidityLookup(models.Model):
    data_validity_comment = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = 'data_validity_lookup'

class DefinedDailyDose(models.Model):
    atc_code = models.ForeignKey(AtcClassification, db_column='atc_code')
    ddd_value = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    ddd_units = models.CharField(max_length=20, blank=True)
    ddd_admr = models.CharField(max_length=20, blank=True)
    ddd_comment = models.CharField(max_length=400, blank=True)
    ddd_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'defined_daily_dose'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'django_site'

class Docs(models.Model):
    doc_id = models.IntegerField(primary_key=True)
    journal = models.CharField(max_length=50, blank=True)
    year = models.SmallIntegerField(null=True, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    first_page = models.CharField(max_length=50, blank=True)
    last_page = models.CharField(max_length=50, blank=True)
    pubmed_id = models.BigIntegerField(unique=True, null=True, blank=True)
    doi = models.CharField(max_length=50, blank=True)
    chembl = models.ForeignKey(ChemblIdLookup)
    title = models.CharField(max_length=500, blank=True)
    doc_type = models.CharField(max_length=50)
    authors = models.CharField(max_length=4000, blank=True)
    abstract = models.TextField(blank=True)
    class Meta:
        db_table = 'docs'

class Domains(models.Model):
    domain_id = models.IntegerField(primary_key=True)
    domain_type = models.CharField(max_length=20)
    source_domain_id = models.CharField(max_length=20)
    domain_name = models.CharField(max_length=20, blank=True)
    domain_description = models.CharField(max_length=500, blank=True)
    class Meta:
        db_table = 'domains'

class DrugMechanism(models.Model):
    mec_id = models.IntegerField(primary_key=True)
    record = models.ForeignKey(CompoundRecords)
    molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='molregno', blank=True)
    mechanism_of_action = models.CharField(max_length=250, blank=True)
    tid = models.ForeignKey('TargetDictionary', null=True, db_column='tid', blank=True)
    site = models.ForeignKey(BindingSites, null=True, blank=True)
    action_type = models.ForeignKey(ActionType, null=True, db_column='action_type', blank=True)
    direct_interaction = models.SmallIntegerField(null=True, blank=True)
    molecular_mechanism = models.SmallIntegerField(null=True, blank=True)
    disease_efficacy = models.SmallIntegerField(null=True, blank=True)
    mechanism_comment = models.CharField(max_length=500, blank=True)
    selectivity_comment = models.CharField(max_length=100, blank=True)
    binding_site_comment = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'drug_mechanism'

class Formulations(models.Model):
    product = models.ForeignKey('Products')
    ingredient = models.CharField(max_length=200, blank=True)
    strength = models.CharField(max_length=200, blank=True)
    record = models.ForeignKey(CompoundRecords)
    molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='molregno', blank=True)
    formulation_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'formulations'

class FpsRdkit(models.Model):
    molregno = models.IntegerField(primary_key=True)
    torsionbv = models.TextField(blank=True) # This field type is a guess.
    mfp2 = models.TextField(blank=True) # This field type is a guess.
    ffp2 = models.TextField(blank=True) # This field type is a guess.
    rdkfp = models.TextField(blank=True) # This field type is a guess.
    atombv = models.TextField(blank=True) # This field type is a guess.
    layeredfp = models.TextField(blank=True) # This field type is a guess.
    maccsfp = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = 'fps_rdkit'

class LigandEff(models.Model):
    activity = models.ForeignKey(Activities, primary_key=True)
    bei = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    sei = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    le = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    lle = models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)
    class Meta:
        db_table = 'ligand_eff'

class MechanismRefs(models.Model):
    mecref_id = models.IntegerField(primary_key=True)
    mec = models.ForeignKey(DrugMechanism)
    ref_type = models.CharField(max_length=50)
    ref_id = models.CharField(max_length=100, blank=True)
    ref_url = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = 'mechanism_refs'

class MolPictures(models.Model):
    molregno = models.IntegerField(primary_key=True)
    image = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = 'mol_pictures'

class MoleculeAtcClassification(models.Model):
    mol_atc_id = models.IntegerField(primary_key=True)
    level5 = models.ForeignKey(AtcClassification, db_column='level5')
    molregno = models.ForeignKey('MoleculeDictionary', db_column='molregno')
    class Meta:
        db_table = 'molecule_atc_classification'

class MoleculeDictionary(models.Model):
    molregno = models.IntegerField(primary_key=True)
    pref_name = models.CharField(max_length=255, blank=True)
    chembl = models.ForeignKey(ChemblIdLookup, unique=True)
    max_phase = models.SmallIntegerField()
    therapeutic_flag = models.SmallIntegerField()
    dosed_ingredient = models.SmallIntegerField()
    structure_type = models.CharField(max_length=10)
    chebi_id = models.IntegerField(unique=True, null=True, blank=True)
    chebi_par_id = models.IntegerField(null=True, blank=True)
    molecule_type = models.CharField(max_length=30, blank=True)
    first_approval = models.SmallIntegerField(null=True, blank=True)
    oral = models.SmallIntegerField()
    parenteral = models.SmallIntegerField()
    topical = models.SmallIntegerField()
    black_box_warning = models.SmallIntegerField()
    natural_product = models.SmallIntegerField()
    first_in_class = models.SmallIntegerField()
    chirality = models.SmallIntegerField()
    prodrug = models.SmallIntegerField()
    inorganic_flag = models.SmallIntegerField()
    usan_year = models.SmallIntegerField(null=True, blank=True)
    availability_type = models.SmallIntegerField(null=True, blank=True)
    usan_stem = models.CharField(max_length=50, blank=True)
    polymer_flag = models.SmallIntegerField(null=True, blank=True)
    usan_substem = models.CharField(max_length=50, blank=True)
    usan_stem_definition = models.CharField(max_length=1000, blank=True)
    indication_class = models.CharField(max_length=1000, blank=True)
    class Meta:
        db_table = 'molecule_dictionary'

class MoleculeHierarchy(models.Model):
    molregno = models.ForeignKey(MoleculeDictionary, primary_key=True, db_column='molregno')
    parent_molregno = models.ForeignKey(MoleculeDictionary, null=True, db_column='parent_molregno', blank=True)
    active_molregno = models.ForeignKey(MoleculeDictionary, null=True, db_column='active_molregno', blank=True)
    class Meta:
        db_table = 'molecule_hierarchy'

class MoleculeSynonyms(models.Model):
    molregno = models.ForeignKey(MoleculeDictionary, db_column='molregno')
    synonyms = models.CharField(max_length=200)
    syn_type = models.CharField(max_length=50)
    molsyn_id = models.IntegerField(primary_key=True)
    res_stem = models.ForeignKey('ResearchStem', null=True, blank=True)
    class Meta:
        db_table = 'molecule_synonyms'

class MolsRdkit(models.Model):
    molregno = models.IntegerField(primary_key=True)
    m = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = 'mols_rdkit'

class OctmpSss332Ec2669E2A1D1226B9718356B379F9(models.Model):
    molregno = models.IntegerField(null=True, blank=True)
    m = models.TextField(blank=True) # This field type is a guess.
    chembl_id = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = 'octmp_sss_332ec2669e2a1d1226b9718356b379f9'

class OctmpSummary(models.Model):
    id = models.DecimalField(max_digits=11, decimal_places=0)
    table_name = models.CharField(max_length=50, blank=True)
    table_created = models.DateTimeField(null=True, blank=True)
    query_md5 = models.CharField(max_length=32, blank=True)
    class Meta:
        db_table = 'octmp_summary'

class OrganismClass(models.Model):
    oc_id = models.IntegerField(primary_key=True)
    tax_id = models.BigIntegerField(unique=True, null=True, blank=True)
    l1 = models.CharField(max_length=200, blank=True)
    l2 = models.CharField(max_length=200, blank=True)
    l3 = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = 'organism_class'

class PfamMaps(models.Model):
    map_id = models.IntegerField(null=True, blank=True)
    activity_id = models.IntegerField(null=True, blank=True)
    compd_id = models.IntegerField(null=True, blank=True)
    domain_name = models.CharField(max_length=100, blank=True)
    category_flag = models.IntegerField(null=True, blank=True)
    status_flag = models.IntegerField(null=True, blank=True)
    manual_flag = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=150, blank=True)
    timestamp = models.CharField(max_length=25, blank=True)
    class Meta:
        db_table = 'pfam_maps'

class PredictedBindingDomains(models.Model):
    predbind_id = models.IntegerField(primary_key=True)
    activity = models.ForeignKey(Activities, null=True, blank=True)
    site = models.ForeignKey(BindingSites, null=True, blank=True)
    prediction_method = models.CharField(max_length=50, blank=True)
    confidence = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'predicted_binding_domains'

class Products(models.Model):
    dosage_form = models.CharField(max_length=200, blank=True)
    route = models.CharField(max_length=200, blank=True)
    trade_name = models.CharField(max_length=200, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    ad_type = models.CharField(max_length=5, blank=True)
    oral = models.SmallIntegerField(null=True, blank=True)
    topical = models.SmallIntegerField(null=True, blank=True)
    parenteral = models.SmallIntegerField(null=True, blank=True)
    black_box_warning = models.SmallIntegerField(null=True, blank=True)
    applicant_full_name = models.CharField(max_length=200, blank=True)
    innovator_company = models.SmallIntegerField(null=True, blank=True)
    product_id = models.CharField(max_length=30, primary_key=True)
    nda_type = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'products'

class ProteinClassSynonyms(models.Model):
    protclasssyn_id = models.IntegerField(primary_key=True)
    protein_class = models.ForeignKey('ProteinClassification')
    protein_class_synonym = models.CharField(max_length=1000, blank=True)
    syn_type = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = 'protein_class_synonyms'

class ProteinClassification(models.Model):
    protein_class_id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField(null=True, blank=True)
    pref_name = models.CharField(max_length=500, blank=True)
    short_name = models.CharField(max_length=50, blank=True)
    protein_class_desc = models.CharField(max_length=410)
    definition = models.CharField(max_length=4000, blank=True)
    class Meta:
        db_table = 'protein_classification'

class ProteinFamilyClassification(models.Model):
    protein_class_id = models.IntegerField(primary_key=True)
    protein_class_desc = models.CharField(max_length=410, unique=True)
    l1 = models.CharField(max_length=50)
    l2 = models.CharField(max_length=50, blank=True)
    l3 = models.CharField(max_length=50, blank=True)
    l4 = models.CharField(max_length=50, blank=True)
    l5 = models.CharField(max_length=50, blank=True)
    l6 = models.CharField(max_length=50, blank=True)
    l7 = models.CharField(max_length=50, blank=True)
    l8 = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'protein_family_classification'

class RelationshipType(models.Model):
    relationship_type = models.CharField(max_length=1, primary_key=True)
    relationship_desc = models.CharField(max_length=250, blank=True)
    class Meta:
        db_table = 'relationship_type'

class ResearchCompanies(models.Model):
    co_stem_id = models.IntegerField(primary_key=True)
    res_stem = models.ForeignKey('ResearchStem', null=True, blank=True)
    company = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    previous_company = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'research_companies'

class ResearchStem(models.Model):
    res_stem_id = models.IntegerField(primary_key=True)
    research_stem = models.CharField(max_length=20, unique=True, blank=True)
    class Meta:
        db_table = 'research_stem'

class SiteComponents(models.Model):
    sitecomp_id = models.IntegerField(primary_key=True)
    site = models.ForeignKey(BindingSites)
    component = models.ForeignKey(ComponentSequences, null=True, blank=True)
    domain = models.ForeignKey(Domains, null=True, blank=True)
    site_residues = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = 'site_components'

class Source(models.Model):
    src_id = models.SmallIntegerField(primary_key=True)
    src_description = models.CharField(max_length=500, blank=True)
    src_short_name = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = 'source'

class TargetComponents(models.Model):
    tid = models.ForeignKey('TargetDictionary', db_column='tid')
    component = models.ForeignKey(ComponentSequences)
    targcomp_id = models.IntegerField(primary_key=True)
    homologue = models.SmallIntegerField()
    class Meta:
        db_table = 'target_components'

class TargetDictionary(models.Model):
    tid = models.IntegerField(primary_key=True)
    target_type = models.ForeignKey('TargetType', null=True, db_column='target_type', blank=True)
    pref_name = models.CharField(max_length=200, blank=True)
    tax_id = models.BigIntegerField(null=True, blank=True)
    organism = models.CharField(max_length=150, blank=True)
    chembl = models.ForeignKey(ChemblIdLookup, null=True, blank=True)
    species_group_flag = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'target_dictionary'

class TargetRelations(models.Model):
    tid = models.ForeignKey(TargetDictionary, db_column='tid')
    relationship = models.CharField(max_length=20)
    related_tid = models.ForeignKey(TargetDictionary, db_column='related_tid')
    targrel_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'target_relations'

class TargetType(models.Model):
    target_type = models.CharField(max_length=30, primary_key=True)
    target_desc = models.CharField(max_length=250, blank=True)
    parent_type = models.CharField(max_length=25, blank=True)
    class Meta:
        db_table = 'target_type'

class TestPfamMaps(models.Model):
    map_id = models.IntegerField(primary_key=True)
    activity_id = models.IntegerField(null=True, blank=True)
    compd_id = models.IntegerField(null=True, blank=True)
    domain_name = models.CharField(max_length=100, blank=True)
    category_flag = models.IntegerField(null=True, blank=True)
    status_flag = models.IntegerField(null=True, blank=True)
    manual_flag = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=150, blank=True)
    timestamp = models.CharField(max_length=25, blank=True)
    class Meta:
        db_table = 'test_pfam_maps'

class Tmp(models.Model):
    assay_id = models.IntegerField(primary_key=True)
    system_label = models.CharField(max_length=-1, blank=True)
    functional_label = models.CharField(max_length=-1, blank=True)
    timestamp = models.CharField(max_length=-1, blank=True)
    comment = models.CharField(max_length=-1, blank=True)
    curator = models.CharField(max_length=-1, blank=True)
    class Meta:
        db_table = 'tmp'

class UsanStems(models.Model):
    stem = models.CharField(max_length=100, primary_key=True)
    stem_class = models.CharField(max_length=100, blank=True)
    annotation = models.CharField(max_length=2000, blank=True)
    major_class = models.CharField(max_length=100, blank=True)
    who_extra = models.CharField(max_length=100, blank=True)
    usan_stem_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'usan_stems'

class Version(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    creation_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = 'version'

