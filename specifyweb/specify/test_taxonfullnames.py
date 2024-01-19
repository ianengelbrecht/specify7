import unittest
from tree_extras_nodjango import predict_taxonname_with_authority


name = 'smithii'
authority = "(F.O. P-Cambridge, 1897)"
ancestors = [
    {"taxonid": 1, "parentid": None, "name": "Life", "rank": "Life", "IsInFullName": 0},
    {"taxonid": 2, "parentid": 1, "name": "Plantae", "rank": "Kingdom", "IsInFullName": 0},
    {"taxonid": 4, "parentid": 2, "name": "Ginkgophyta", "rank": "Division", "IsInFullName": 0},
    {"taxonid": 5, "parentid": 4, "name": "Ginkgoaceae", "rank": "Family", "IsInFullName": 0},
    {"taxonid": 6, "parentid": 5, "name": "Ginkgo", "rank": "Genus", "IsInFullName": 1}
]

class TestTaxonFullName(unittest.TestCase):

    def test_ancestors_in_fullname_if_isinfullname(self):
        """Any ancestors with isInFullName must be in the fullname"""
        fullname = predict_taxonname_with_authority(name, authority, ancestors)
        ancestors_in_fullname = [x["taxonname"] in fullname for x in ancestors if x["IsInFullName"] == 1]
        self.assertTrue(all(ancestors_in_fullname))


    def test_name_is_in_fullname(self):
        """If we are using this function then the name must be in fullname"""
        fullname = predict_taxonname_with_authority(name, authority, ancestors)
        self.assertTrue(name in fullname)

    def test_name_is_in_fullname(self):
        """If there is an authority it must be in fullname"""
        fullname = predict_taxonname_with_authority(name, authority, ancestors)
        self.assertTrue(authority in fullname)
    
    # THE FOLLOWING TESTS ARE FOR PLANT/FUNGI NAMES ONLY

    def test_isHybrid_has_x_for_plants(self):
        """If isHybrid is true, there must be a multiplication sign in front of the name, with a space""" #note that the space is not required by the code, but will be used as the convention here
        return False

    def authorities_only_added_if_preferred(self):
        """If preference is to include authorities, and an authority string exists, it must be in the fullname"""
        return False
    
    def authority_comes_last_if_not_autonym(self):
        return False
    
    def authority_comes_after_first_epithet_if_autonym(self):
        """For autonyms/nominotypical taxa the authority must be after the first instance of the repeated epithet"""
        return False
    
    #this is only for an HTML name. Note Specify also has a cultivarName field, which people are likely using for this purpose
    # def names_with_quotes_are_not_italicized(self):
    #     return False
    
    def subspecies_include_abbreviation_subsp(self):
        return False
    
    def varieties_include_abbreviation_var(self):
        return False
    
    def subvarieties_include_abbreviation_subvar(self):
        return False
    
    def forms_include_abbreviation_f(self):
        return False
    
    def subforms_include_abbreviation_subf(self):
        return False
    

    

if __name__ == '__main__':
    unittest.main()