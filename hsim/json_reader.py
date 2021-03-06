import json
from hsim import cli

class HtanJsonReader:
    """
    Utility Class for Reading in HTAN JSON File.
    """

    def __init__(self, json_file_name, template_list):
        self.error_list = []
        self.json_file_name = json_file_name
        fd = open(json_file_name, "r")
        self.doc = json.load(fd)
        self.__load_schema()

        # Check Links for All Assays
        for template in template_list:
            if template[1] == cli.ASSAY_TYPE:
                self.__check_assay_links(template[0].replace("bts:", ""))

        # Check the Biospecimen Links
        self.__check_biospecimen_links()

    def get_doc(self):
        """
        Get the Loaded JSON Doc.
        """
        return self.doc

    def get_error_list(self):
        """
        Get the Error List.
        """
        return self.error_list

    def get_num_atlases(self):
        """
        Get Total Number of Atlases Loaded.
        """
        atlas_list = self.doc["atlases"]
        return len(atlas_list)

    def get_attribute_index(self, list_name, attribute_name):
        """
        Get the index value for the specified list and attribute pair.
        """
        return self.schema_dict[list_name][attribute_name]

    def __load_schema(self):
        """
        Load the Schemas into Various Hashes for Quick Look up Later.
        """
        schema_list = self.doc["schemas"]
        self.schema_dict = {}
        for schema in schema_list:
            schema_name = schema["data_schema"]
            attribute_list = schema["attributes"]
            index_counter = 0
            name_dict = {}
            for attribute in attribute_list:
                id = attribute["id"]
                name_dict[id] = index_counter
                index_counter += 1
            self.schema_dict[schema_name] = name_dict

    def __extract_sample_ids(self, atlas):
        """
        Extract the Sample IDs.
        """
        sample_id_list = []
        biospecimen_list = "Biospecimen"
        attribute_index = self.get_attribute_index(biospecimen_list, "bts:HTANBiospecimenID")
        record_list = atlas[biospecimen_list]["record_list"]
        for record in record_list:
            sample_id = record[attribute_index]
            sample_id_list.append(sample_id)
        return sample_id_list

    def __extract_participant_ids(self, atlas):
        """
        Extract the Participant IDs.
        """
        participant_id_list = []
        biospecimen_list = "Demographics"
        attribute_index = self.get_attribute_index(biospecimen_list, "bts:HTANParticipantID")
        record_list = atlas[biospecimen_list]["record_list"]
        for record in record_list:
            participant_id = record[attribute_index]
            participant_id_list.append(participant_id)
        return participant_id_list        

    def __check_assay_links(self, list_name):
        """
        Check Assay Links.
        """
        atlas_list = self.doc["atlases"]
        target_id = "bts:HTANParentBiospecimenID"
        attribute_index = self.get_attribute_index(list_name, target_id)
        for atlas in atlas_list:
            sample_id_list = self.__extract_sample_ids(atlas)
            record_list = atlas[list_name]["record_list"]
            for record in record_list:
                biospecimen_id = record[attribute_index]
                if biospecimen_id not in sample_id_list:
                    self.error_list.append(
                        "Within %s, we have %s:%s, but this ID does not exist within the Biospecimen list."
                        % (list_name, target_id, biospecimen_id)
                    )

    def __check_biospecimen_links(self):
        """
        Check Biospecimen Links.
        """
        atlas_list = self.doc["atlases"]
        target_id = "bts:HTANParentID"
        list_name = "Biospecimen"
        attribute_index = self.get_attribute_index(list_name, target_id)
        for atlas in atlas_list:
            participant_id_list = self.__extract_participant_ids(atlas)
            sample_id_list = self.__extract_sample_ids(atlas)
            record_list = atlas[list_name]["record_list"]
            for record in record_list:
                parent_id = record[attribute_index]
                if parent_id not in participant_id_list and parent_id not in sample_id_list:
                    msg = "Within %s, we have %s:%s, but this ID does not exist within " \
                        "the Biospecimen or Demographics list." % (list_name, target_id, parent_id)
                    self.error_list.append(msg)