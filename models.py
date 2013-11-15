# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Activities(models.Model):
    activity_id = models.IntegerField(primary_key=True)
    assay = models.ForeignKey('Assays')
    doc = models.ForeignKey('Docs', null=True, blank=True)
    record = models.ForeignKey('CompoundRecords')
    molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='molregno', blank=True)
    standard_relation = models.CharField(max_length=150, blank=True)
    published_value = models.FloatField(null=True, blank=True)
    published_units = models.CharField(max_length=300, blank=True)
    standard_value = models.FloatField(null=True, blank=True)
    standard_units = models.CharField(max_length=300, blank=True)
    standard_flag = models.IntegerField(null=True, blank=True)
    standard_type = models.CharField(max_length=750, blank=True)
    activity_comment = models.CharField(max_length=765, blank=True)
    published_type = models.CharField(max_length=750, blank=True)
    data_validity_comment = models.ForeignKey('DataValidityLookup', null=True, db_column='data_validity_comment', blank=True)
    potential_duplicate = models.IntegerField(null=True, blank=True)
    published_relation = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'activities'

class ActivityStdsLookup(models.Model):
    std_act_id = models.IntegerField(primary_key=True)
    standard_type = models.CharField(max_length=750)
    definition = models.TextField(blank=True)
    standard_units = models.CharField(max_length=300)
    normal_range_min = models.FloatField(null=True, blank=True)
    normal_range_max = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'activity_stds_lookup'

class AssayType(models.Model):
    assay_type = models.CharField(max_length=3, primary_key=True)
    assay_desc = models.CharField(max_length=750, blank=True)
    class Meta:
        db_table = u'assay_type'

class Assays(models.Model):
    assay_id = models.IntegerField(primary_key=True)
    doc = models.ForeignKey('Docs')
    description = models.TextField(blank=True)
    assay_type = models.ForeignKey('AssayType', null=True, db_column='assay_type', blank=True)
    assay_test_type = models.CharField(max_length=60, blank=True)
    assay_category = models.CharField(max_length=60, blank=True)
    assay_organism = models.CharField(max_length=750, blank=True)
    assay_tax_id = models.IntegerField(null=True, blank=True)
    assay_strain = models.CharField(max_length=600, blank=True)
    assay_tissue = models.CharField(max_length=300, blank=True)
    assay_cell_type = models.CharField(max_length=300, blank=True)
    assay_subcellular_fraction = models.CharField(max_length=300, blank=True)
    tid = models.ForeignKey('TargetDictionary', null=True, db_column='tid', blank=True)
    relationship_type = models.ForeignKey('RelationshipType', null=True, db_column='relationship_type', blank=True)
    confidence_score = models.ForeignKey('ConfidenceScoreLookup', null=True, db_column='confidence_score', blank=True)
    curated_by = models.ForeignKey('CurationLookup', null=True, db_column='curated_by', blank=True)
    src = models.ForeignKey('Source')
    src_assay_id = models.CharField(max_length=150, blank=True)
    chembl = models.ForeignKey('ChemblIdLookup')
    class Meta:
        db_table = u'assays'

class AtcClassification(models.Model):
    who_name = models.CharField(max_length=450, blank=True)
    level1 = models.CharField(max_length=30, blank=True)
    level2 = models.CharField(max_length=30, blank=True)
    level3 = models.CharField(max_length=30, blank=True)
    level4 = models.CharField(max_length=30, blank=True)
    level5 = models.CharField(max_length=30, primary_key=True)
    who_id = models.CharField(max_length=45, blank=True)
    level1_description = models.CharField(max_length=450, blank=True)
    level2_description = models.CharField(max_length=450, blank=True)
    level3_description = models.CharField(max_length=450, blank=True)
    level4_description = models.CharField(max_length=450, blank=True)
    molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='molregno', blank=True)
    class Meta:
        db_table = u'atc_classification'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=240)
    class Meta:
        db_table = u'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey('AuthGroup')
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = u'auth_group_permissions'

class AuthMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('AuthUser')
    message = models.TextField()
    class Meta:
        db_table = u'auth_message'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=300)
    class Meta:
        db_table = u'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=90)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=384)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = u'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('AuthUser')
    group = models.ForeignKey('AuthGroup')
    class Meta:
        db_table = u'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('AuthUser')
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = u'auth_user_user_permissions'

class Binding(models.Model):
    standard_value = models.FloatField(null=True, blank=True)
    standard_type = models.CharField(max_length=750, blank=True)
    standard_units = models.CharField(max_length=300, blank=True)
    standard_relation = models.CharField(max_length=150, blank=True)
    activity_id = models.IntegerField()
    class Meta:
        db_table = u'binding'

class BindingSites(models.Model):
    site_id = models.IntegerField(primary_key=True)
    site_name = models.CharField(max_length=600, blank=True)
    tid = models.ForeignKey('TargetDictionary', null=True, db_column='tid', blank=True)
    class Meta:
        db_table = u'binding_sites'

class BioComponentSequences(models.Model):
    component_id = models.IntegerField(primary_key=True)
    component_type = models.CharField(max_length=150)
    description = models.CharField(max_length=600, blank=True)
    sequence = models.TextField(blank=True)
    sequence_md5sum = models.CharField(max_length=96, blank=True)
    tax_id = models.IntegerField(null=True, blank=True)
    organism = models.CharField(max_length=450, blank=True)
    class Meta:
        db_table = u'bio_component_sequences'

class BiotherapeuticComponents(models.Model):
    biocomp_id = models.IntegerField(primary_key=True)
    molregno = models.ForeignKey('Biotherapeutics', db_column='molregno')
    component = models.ForeignKey('BioComponentSequences')
    class Meta:
        db_table = u'biotherapeutic_components'

class Biotherapeutics(models.Model):
    molregno = models.ForeignKey('MoleculeDictionary', db_column='molregno')
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'biotherapeutics'

class CellDictionary(models.Model):
    cell_id = models.IntegerField(primary_key=True)
    cell_name = models.CharField(unique=True, max_length=150)
    cell_description = models.CharField(max_length=600, blank=True)
    cell_source_tissue = models.CharField(max_length=150, blank=True)
    cell_source_organism = models.CharField(max_length=450, blank=True)
    cell_source_tax_id = models.IntegerField(unique=True, null=True, blank=True)
    class Meta:
        db_table = u'cell_dictionary'

class ChemblIdLookup(models.Model):
    chembl_id = models.CharField(max_length=60, primary_key=True)
    entity_type = models.CharField(unique=True, max_length=150, blank=True)
    entity_id = models.IntegerField(unique=True, null=True, blank=True)
    status = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'chembl_id_lookup'

class ComponentClass(models.Model):
    component = models.ForeignKey('ComponentSequences')
    protein_class = models.ForeignKey('ProteinFamilyClassification')
    comp_class_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'component_class'

class ComponentDomains(models.Model):
    compd_id = models.IntegerField(primary_key=True)
    domain = models.ForeignKey('Domains', null=True, blank=True)
    component = models.ForeignKey('ComponentSequences')
    start_position = models.IntegerField(unique=True, null=True, blank=True)
    end_position = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'component_domains'

class ComponentSequences(models.Model):
    component_id = models.IntegerField(primary_key=True)
    component_type = models.CharField(max_length=150, blank=True)
    accession = models.CharField(unique=True, max_length=75, blank=True)
    sequence = models.TextField(blank=True)
    sequence_md5sum = models.CharField(max_length=96, blank=True)
    description = models.CharField(max_length=600, blank=True)
    tax_id = models.IntegerField(null=True, blank=True)
    organism = models.CharField(max_length=450, blank=True)
    db_source = models.CharField(max_length=75, blank=True)
    db_version = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'component_sequences'

class ComponentSynonyms(models.Model):
    compsyn_id = models.IntegerField(primary_key=True)
    component = models.ForeignKey('ComponentSequences')
    component_synonym = models.CharField(max_length=600, blank=True)
    syn_type = models.CharField(unique=True, max_length=60, blank=True)
    class Meta:
        db_table = u'component_synonyms'

class CompoundProperties(models.Model):
    molregno = models.ForeignKey('MoleculeDictionary', db_column='molregno')
    mw_freebase = models.FloatField(null=True, blank=True)
    alogp = models.FloatField(null=True, blank=True)
    hba = models.IntegerField(null=True, blank=True)
    hbd = models.IntegerField(null=True, blank=True)
    psa = models.FloatField(null=True, blank=True)
    rtb = models.IntegerField(null=True, blank=True)
    ro3_pass = models.CharField(max_length=9, blank=True)
    num_ro5_violations = models.IntegerField(null=True, blank=True)
    med_chem_friendly = models.CharField(max_length=9, blank=True)
    acd_most_apka = models.FloatField(null=True, blank=True)
    acd_most_bpka = models.FloatField(null=True, blank=True)
    acd_logp = models.FloatField(null=True, blank=True)
    acd_logd = models.FloatField(null=True, blank=True)
    molecular_species = models.CharField(max_length=150, blank=True)
    full_mwt = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'compound_properties'

class CompoundRecords(models.Model):
    record_id = models.IntegerField(primary_key=True)
    molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='molregno', blank=True)
    doc = models.ForeignKey('Docs')
    compound_key = models.CharField(max_length=750, blank=True)
    compound_name = models.TextField(blank=True)
    src = models.ForeignKey('Source')
    src_compound_id = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'compound_records'

class CompoundStructures(models.Model):
    molregno = models.ForeignKey('MoleculeDictionary', db_column='molregno')
    molfile = models.TextField(blank=True)
    standard_inchi = models.TextField(blank=True)
    standard_inchi_key = models.CharField(unique=True, max_length=81)
    canonical_smiles = models.TextField(blank=True)
    molformula = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'compound_structures'

class ConfidenceScoreLookup(models.Model):
    confidence_score = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=300)
    target_mapping = models.CharField(max_length=90)
    class Meta:
        db_table = u'confidence_score_lookup'

class CurationLookup(models.Model):
    curated_by = models.CharField(max_length=60, primary_key=True)
    description = models.CharField(max_length=300)
    class Meta:
        db_table = u'curation_lookup'

class DataValidityLookup(models.Model):
    data_validity_comment = models.CharField(max_length=90, primary_key=True)
    description = models.CharField(max_length=600, blank=True)
    class Meta:
        db_table = u'data_validity_lookup'

class DefinedDailyDose(models.Model):
    atc_code = models.ForeignKey('AtcClassification', db_column='atc_code')
    ddd_value = models.FloatField(null=True, blank=True)
    ddd_units = models.CharField(max_length=60, blank=True)
    ddd_admr = models.CharField(max_length=60, blank=True)
    ddd_comment = models.TextField(blank=True)
    ddd_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'defined_daily_dose'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey('AuthUser')
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=600)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = u'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    app_label = models.CharField(max_length=300)
    model = models.CharField(max_length=300)
    class Meta:
        db_table = u'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=120, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=300)
    name = models.CharField(max_length=150)
    class Meta:
        db_table = u'django_site'

class Docs(models.Model):
    doc_id = models.IntegerField(primary_key=True)
    journal = models.CharField(max_length=150, blank=True)
    year = models.IntegerField(null=True, blank=True)
    volume = models.CharField(max_length=150, blank=True)
    issue = models.CharField(max_length=150, blank=True)
    first_page = models.CharField(max_length=150, blank=True)
    last_page = models.CharField(max_length=150, blank=True)
    pubmed_id = models.IntegerField(null=True, blank=True)
    doi = models.CharField(max_length=150, blank=True)
    chembl = models.ForeignKey('ChemblIdLookup')
    title = models.TextField(blank=True)
    doc_type = models.CharField(max_length=150)
    authors = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    class Meta:
        db_table = u'docs'

class Domains(models.Model):
    domain_id = models.IntegerField(primary_key=True)
    domain_type = models.CharField(max_length=60)
    source_domain_id = models.CharField(max_length=60)
    domain_name = models.CharField(max_length=60, blank=True)
    domain_description = models.TextField(blank=True)
    class Meta:
        db_table = u'domains'

class Formulations(models.Model):
    product = models.ForeignKey('Products')
    ingredient = models.CharField(max_length=600, blank=True)
    strength = models.CharField(max_length=600, blank=True)
    record = models.ForeignKey('CompoundRecords')
    molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='molregno', blank=True)
    formulation_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'formulations'

class LigandEff(models.Model):
    activity = models.ForeignKey('Activities')
    bei = models.FloatField(null=True, blank=True)
    sei = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'ligand_eff'

class MoleculeDictionary(models.Model):
    molregno = models.IntegerField(primary_key=True)
    pref_name = models.CharField(max_length=765, blank=True)
    chembl = models.ForeignKey('ChemblIdLookup')
    max_phase = models.IntegerField()
    therapeutic_flag = models.IntegerField()
    dosed_ingredient = models.IntegerField()
    structure_type = models.CharField(max_length=30)
    chebi_id = models.IntegerField(null=True, blank=True)
    chebi_par_id = models.IntegerField(null=True, blank=True)
    molecule_type = models.CharField(max_length=90, blank=True)
    first_approval = models.IntegerField(null=True, blank=True)
    oral = models.IntegerField()
    parenteral = models.IntegerField()
    topical = models.IntegerField()
    black_box_warning = models.IntegerField()
    natural_product = models.IntegerField()
    first_in_class = models.IntegerField()
    chirality = models.IntegerField()
    prodrug = models.IntegerField()
    inorganic_flag = models.IntegerField()
    usan_year = models.IntegerField(null=True, blank=True)
    availability_type = models.IntegerField(null=True, blank=True)
    usan_stem = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'molecule_dictionary'


class MoleculeHierarchy(models.Model):


    molecule = models.OneToOneField(MoleculeDictionary, unique=True, db_column='molregno', primary_key=True,
        help_text="Foreign key to compounds table. This field holds a list of all of the ChEMBL compounds with associated data (e.g., activity information, approved drugs). Parent compounds that are generated only by removing salts, and which do not themselves have any associated data will not appear here.")
    parent_molecule = models.ForeignKey(MoleculeDictionary, null=True, db_column='parent_molregno', blank=True,
        related_name="parents",
        help_text="Represents parent compound of molregno in first field (i.e., generated by removing salts). Where molregno and parent_molregno are same, the initial ChEMBL compound did not contain a salt component, or else could not be further processed for various reasons (e.g., inorganic mixture). Compounds which are only generated by removing salts will appear in this field only. Those which, themselves, have any associated data (e.g., activity data) or are launched drugs will also appear in the molregno field.")
    active_molecule = models.ForeignKey(MoleculeDictionary, null=True, blank=True, related_name="active",
        db_column='active_molregno',
        help_text="Where a compound is a pro-drug, this represents the active metabolite of the 'dosed' compound given by parent_molregno. Where parent_molregno and active_molregno are the same, the compound is not currently known to be a pro-drug. ")

    class Meta:
        db_table = u'MoleculeHierarchy'

#class MoleculeHierarchy(models.Model):
#    molregno = models.ForeignKey('MoleculeDictionary', db_column='molregno')
#    parent_molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='parent_molregno', blank=True)
#    active_molregno = models.ForeignKey('MoleculeDictionary', null=True, db_column='active_molregno', blank=True)
#    class Meta:
#        db_table = u'molecule_hierarchy'

class MoleculeSynonyms(models.Model):
    molregno = models.ForeignKey('MoleculeDictionary', db_column='molregno')
    synonyms = models.CharField(max_length=600)
    syn_type = models.CharField(unique=True, max_length=150)
    molsyn_id = models.IntegerField(primary_key=True)
    res_stem = models.ForeignKey('ResearchStem', null=True, blank=True)
    class Meta:
        db_table = u'molecule_synonyms'

class OrganismClass(models.Model):
    oc_id = models.IntegerField(primary_key=True)
    tax_id = models.IntegerField(unique=True, null=True, blank=True)
    l1 = models.CharField(max_length=600, blank=True)
    l2 = models.CharField(max_length=600, blank=True)
    l3 = models.CharField(max_length=600, blank=True)
    class Meta:
        db_table = u'organism_class'

class PfamMaps(models.Model):
    map_id = models.IntegerField(primary_key=True)
    activity_id = models.IntegerField(null=True, blank=True)
    compd_id = models.IntegerField(null=True, blank=True)
    domain_name = models.CharField(max_length=300, blank=True)
    category_flag = models.IntegerField(null=True, blank=True)
    status_flag = models.IntegerField(null=True, blank=True)
    manual_flag = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=450, blank=True)
    timestamp = models.CharField(max_length=75, blank=True)
    class Meta:
        db_table = u'pfam_maps'

class PredictedBindingDomains(models.Model):
    predbind_id = models.IntegerField(primary_key=True)
    activity = models.ForeignKey('Activities', null=True, blank=True)
    site = models.ForeignKey('BindingSites', null=True, blank=True)
    prediction_method = models.CharField(max_length=150, blank=True)
    confidence = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'predicted_binding_domains'

class Products(models.Model):
    dosage_form = models.CharField(max_length=600, blank=True)
    route = models.CharField(max_length=600, blank=True)
    trade_name = models.CharField(max_length=600, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    ad_type = models.CharField(max_length=15, blank=True)
    oral = models.IntegerField(null=True, blank=True)
    topical = models.IntegerField(null=True, blank=True)
    parenteral = models.IntegerField(null=True, blank=True)
    black_box_warning = models.IntegerField(null=True, blank=True)
    applicant_full_name = models.CharField(max_length=600, blank=True)
    innovator_company = models.IntegerField(null=True, blank=True)
    product_id = models.CharField(max_length=90, primary_key=True)
    nda_type = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'products'

class ProteinFamilyClassification(models.Model):
    protein_class_id = models.IntegerField(primary_key=True)
    protein_class_desc = models.CharField(max_length=600)
    l1 = models.CharField(unique=True, max_length=150)
    l2 = models.CharField(unique=True, max_length=150, blank=True)
    l3 = models.CharField(unique=True, max_length=150, blank=True)
    l4 = models.CharField(unique=True, max_length=150, blank=True)
    l5 = models.CharField(unique=True, max_length=150, blank=True)
    l6 = models.CharField(unique=True, max_length=150, blank=True)
    l7 = models.CharField(unique=True, max_length=150, blank=True)
    l8 = models.CharField(unique=True, max_length=150, blank=True)
    class Meta:
        db_table = u'protein_family_classification'

class RelationshipType(models.Model):
    relationship_type = models.CharField(max_length=3, primary_key=True)
    relationship_desc = models.CharField(max_length=750, blank=True)
    class Meta:
        db_table = u'relationship_type'

class ResearchCompanies(models.Model):
    co_stem_id = models.IntegerField(primary_key=True)
    res_stem = models.ForeignKey('ResearchStem', null=True, blank=True)
    company = models.CharField(max_length=300, blank=True)
    country = models.CharField(max_length=150, blank=True)
    previous_company = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'research_companies'

class ResearchStem(models.Model):
    res_stem_id = models.IntegerField(primary_key=True)
    research_stem = models.CharField(unique=True, max_length=60, blank=True)
    class Met:
        db_table = u'research_stem'

class SiteComponents(models.Model):
    sitecomp_id = models.IntegerField(primary_key=True)
    site = models.ForeignKey('BindingSites')
    component = models.ForeignKey('ComponentSequences', null=True, blank=True)
    domain = models.ForeignKey('Domains', null=True, blank=True)
    site_residues = models.TextField(blank=True)
    class Meta:
        db_table = u'site_components'

class Source(models.Model):
    src_id = models.IntegerField(primary_key=True)
    src_description = models.TextField(blank=True)
    src_short_name = models.CharField(max_length=60, blank=True)
    class Meta:
        db_table = u'source'

class TargetComponents(models.Model):
    tid = models.ForeignKey('TargetDictionary', db_column='tid')
    component = models.ForeignKey('ComponentSequences')
    targcomp_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'target_components'

class TargetDictionary(models.Model):
    tid = models.IntegerField(primary_key=True)
    target_type = models.ForeignKey('TargetType', null=True, db_column='target_type', blank=True)
    pref_name = models.CharField(max_length=600, blank=True)
    tax_id = models.IntegerField(null=True, blank=True)
    organism = models.CharField(max_length=450, blank=True)
    chembl = models.ForeignKey('ChemblIdLookup', null=True, blank=True)
    class Meta:
        db_table = u'target_dictionary'

class TargetType(models.Model):
    target_type = models.CharField(max_length=90, primary_key=True)
    target_desc = models.CharField(max_length=750, blank=True)
    parent_type = models.CharField(max_length=75, blank=True)
    class Meta:
        db_table = u'target_type'

class UsanStems(models.Model):
    stem = models.CharField(max_length=255, primary_key=True)
    stem_class = models.CharField(max_length=300, blank=True)
    annotation = models.TextField(blank=True)
    major_class = models.CharField(max_length=300, blank=True)
    who_extra = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'usan_stems'

class Version(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'version'

