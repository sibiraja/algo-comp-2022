import numpy as np
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    #TEST COMMENT

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    # Set the incompatible gender/indentity preference combinations to be 0
    # Look at each person's gender preferences, then iterate through the list of genders, and keep track of the indexes at which the gender does not match

    i = 0
    j = 0

    # male = man, nonbinary
    # female = women, nonbinary
    # bisexual = man, woman, nonbinary

    for i in range(len(gender_pref) - 1):
        current_pref = gender_pref[i]
        
        for j in range(len(gender_id) - 1):
            if current_pref == "Men":
                if gender_id[j] == "Female":
                    scores[i][j] = 0
            if current_pref == "Women":
                if gender_id[j] != "Male":
                    scores[i][j] = 0
            # No need to do if statement for people with bisexual preferences because they can get matched up with anyone    
    

    # Split people into two lists. 1 list serves as the propsers and 1 list serves as the receivers
    middle_index = len(gender_id) // 2

    proposers = gender_id[:middle_index]
    
    recievers = gender_id[middle_index:]

    
    
    # Notes about the algorithm about to be implemented:
    # ==================================================
    # Matches are being stored in a list of tuples

    # I need to keep track of whether or not a person has a match yet --> a boolean value may be useful for this
    # --> I could create a list called cuffed that stores boolean values for every person. Each index of the cuffed list corresponds to the index of each person
    # I need to keep track of a person's current match
    # --> I can store every match in matches. If I need to delete a match, I will just delete the tuple within the list. 
    # --> I can store every proposal that is attempted in a matrix. Then, I can check if future proposals are in that matrix.
        #  If they are, then the proposal should not be made because it has already been attempted.
    
    # To keep track of the proposers that initially had a match, but someone else took their partner, I will change their boolean value from True to False in the cuffed list
    
    matches = [()]

    proposals_made = [ [] for k in range(len(proposers) - 1)]

    cuffed = []
    for l in range(len(gender_id) - 1):
        cuffed.append(False)


    # GALE-SHAPLEY ALGORITHM
    # ========================================

    # Require: Initialize each person to be free (unmatched)
    # while Some man is free and hasn’t proposed to every woman do
    #     Choose such a man m
    #     w ← 1st woman on m’s list to whom m has not yet proposed
    #     if w is free then
    #         Match m and w
    #     else if w prefers m to her current match m′
    #         then
    #         Match m and w, and free up m′
    #     else
    #         w rejects m
    #     end if
    # end while

    # IMPLEMENTATION OF THE ALGORITHM BELOW

    # While some proposer is free
    while False in cuffed[:middle_index]:
        current_proposer_index = cuffed.index(False)
        # If the proposer hasn't proposed to every reciever
        if (len(proposals_made[current_proposer_index]) != len(recievers)):
            # Copy the score preferences of the current proposer into a temporary list
            temp_scores = scores[current_proposer_index]

            # for m in range(len(scores[current_proposer_index] - 1)):
            #     temp_scores.append(scores[current_proposer_index][m])

            # for m in scores[current_proposer_index]:
            #     temp_scores.append(scores[current_proposer_index][m])
            
            index_of_reciever = 0
            # PUT THE FOLLOWING IN A WHILE LOOP:
            while True:
                # Find the index of the highest preference that the current proposer has
                max_value = max(temp_scores)
                index_of_reciever = temp_scores.index(max_value)
                
                # If the current proposer has proposed to the highest preferred reciever, then remove that reciever from the temporary list to find the index of the next-preferred reciever
                if index_of_reciever in proposals_made[current_proposer_index]:
                    del temp_scores[index_of_reciever]
                else:
                    break
            
            # If the reciever is not already matched, then match the reciever with the proposer
            if cuffed[index_of_reciever] == False:
                # Update cuffed status of both proposer and reciever
                cuffed[index_of_reciever] == True
                cuffed[current_proposer_index] == True
                # Add the proposal to the proposal_made list
                proposals_made[current_proposer_index].append(index_of_reciever)
                # Update this match in the matches list-of-tuples
                temp_tuple = (current_proposer_index, index_of_reciever)
                matches.append(temp_tuple)
            # If the reciever is matched
            elif cuffed[index_of_reciever] == True:

                # Find the index of the person that the reciever is already matched with
                index_of_existing_proposer = 0
                for n in matches:
                    if matches[n][0] == index_of_reciever:
                        index_of_existing_proposer = matches[n][1]
                    if matches[n][1] == index_of_reciever:
                        index_of_existing_proposer = matches[n][0]

                # If the reciever prefers the current proposer to her existing match
                if scores[index_of_reciever][current_proposer_index] > [index_of_reciever][index_of_existing_proposer]:
                    # Update cuffed status of current proposer and the person that is getting dumped
                    cuffed[index_of_existing_proposer] = False
                    cuffed[current_proposer_index] = True

                    # Find the index of the already-existing match
                    for o in matches:
                        if matches[n][0] == index_of_reciever:
                            index_of_existing_match = n
                        if matches[n][1] == index_of_reciever:
                            index_of_existing_match = n

                    # Delete the already-existing match from matches[()]   
                    del matches[n]

                    # Add new match
                    temp_tuple = (current_proposer_index, index_of_reciever)
                    matches.append(temp_tuple)

                    # Add proposals made
                    proposals_made[current_proposer_index].append(index_of_reciever)
            
            # The reciever rejects the current proposer
            else:

                # Update proposals made
                proposals_made[current_proposer_index].append(index_of_reciever)
              

        # End of original if loop -- This else statement should not execute if the matching is stable
        else:
            break

    # End of while loop

    # Delete empty first element of matches
    del matches[0]

    # Return matches
    return matches    
    


if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)