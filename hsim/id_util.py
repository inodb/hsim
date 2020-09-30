"""
Utility Functions for Generating and Managing HTAN Identifiers.
"""
PARTICIPANT = "PARTICIPANT"
SAMPLE = "SAMPLE"

def generate_htan_participant_ids(htan_id, num_ids):
    """Generate N Participant IDs for the Specified HTAN Atlas."""
    id_list = []
    for x in range(num_ids):
        id_list.append("%s_%d" % (htan_id, x))
    return id_list


def generate_sample_ids(participant_id, num_ids):
    """Generate N Samples IDs from the Specified Participant ID."""
    id_list = []
    for x in range(num_ids):
        id_list.append("%s_%d" % (participant_id, x))
    return id_list


def generate_id_set(htan_id, num_participants, num_samples_per_participant):
    """Generate Simulated ID Set."""
    id_table = []
    participant_id_list = generate_htan_participant_ids(htan_id, num_participants)

    # Table is of the form:
    # 0 - SAMPLE OR PARTICIPANT
    # 1 - HTAN ID
    # 2 - Parent HTAN ID
    for participant_id in participant_id_list:
        id_table.append([PARTICIPANT, participant_id, "-"])
        sample_id_list = generate_sample_ids(
            participant_id, num_samples_per_participant
        )

        counter = 0
        parent_id = participant_id
        for sample_id in sample_id_list:
            id_table.append([SAMPLE, sample_id, parent_id])
            if counter % 2 == 0:
                parent_id = sample_id
            else:
                parent_id = participant_id

    return id_table

def extract_participant_id_list (id_table):
    """Extract Participant ID List from ID Set Table."""
    participant_id_list = []
    for row in id_table:
        if row[0] == PARTICIPANT:
            participant_id_list.append(row[1])
    return participant_id_list

def extract_sample_id_list (id_table):
    """Extract Sample ID List from ID Set Table."""
    sample_id_list = []
    for row in id_table:
        if row[0] == SAMPLE:
            sample_id_list.append(row[1])
    return sample_id_list

def extract_parent_id (id_table, target_id):
    """Extract Parent ID of Target from ID Set Table."""
    for row in id_table:
        if row[1] == target_id:
            return row[2]