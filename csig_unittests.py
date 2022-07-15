import numpy as np
import sys
import csig_gui     as cg
import csig_btn     as cb
import csig_logic   as cl
import csig_def     as cd
import csig_np     as cn
import signal_game  as sig

latest_testchar = "F"

# Increment
def testA_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    
    incr = 0
    for i, i_entry in enumerate(test_matrix):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): 
                test_matrix[i][j][k] = incr
                incr = incr + 1
    cn.fill_nature_half(test_matrix_nature)
    return test_matrix, test_matrix_nature

# Semi-decrement
def testB_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    incr = 0
    for i, i_entry in enumerate(test_matrix):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): 
                test_matrix[i][j][k] = incr
                incr = incr + 1
    test_matrix = test_matrix[::-1]
    cn.fill_nature_half(test_matrix_nature)
    return test_matrix, test_matrix_nature

# Full-decrement
def testC_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    incr = 16
    for i, i_entry in enumerate(test_matrix):
        for j, j_entry in enumerate(i_entry):
            for k, k_entry in enumerate(j_entry): 
                test_matrix[i][j][k] = incr
                incr = incr - 1
    cn.fill_nature_half(test_matrix_nature)
    return test_matrix, test_matrix_nature
    
# All zeros
def testD_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    cn.fill_nature_half(test_matrix_nature)
    return test_matrix, test_matrix_nature

# Pooling SEPR_A
def testE_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    test_matrix = np.array([
        [(15,  4),(30, 11)],
        [(25, 89),( 0,  3)],
        [(10,  2),(17,  0)],
        [( 8,  5),( 9,  4)]
        ])
    cn.fill_nature_half(test_matrix_nature)
    return test_matrix, test_matrix_nature

def testF_gen(parent_in, test_name, test_matrix, test_matrix_nature):    
    test_matrix = np.array([
        [(52, 46), ( 1, 52)],
        [(94, 92), (96, 48)],
        [(52, 74), (97, 33)],
        [(69, 43), (73,  0)]
        ])
    test_matrix_nature = np.array([
        [0.84, 0.16]
        ])
    return test_matrix, test_matrix_nature

def testG_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    test_matrix = np.array([
        [(45, 46), (91, 72)],
        [(49, 26), (25, 21)],
        [(76, 81), (81, 65)],
        [(10, 29), (10, 89)],
        ])
    test_matrix_nature = np.array([
        [0.03, 0.97]
        ])
    return test_matrix, test_matrix_nature

def testH_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    return test_matrix, test_matrix_nature
def testI_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    return test_matrix, test_matrix_nature
def testJ_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    return test_matrix, test_matrix_nature
def testK_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    return test_matrix, test_matrix_nature
def testL_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    return test_matrix, test_matrix_nature
def testM_gen(parent_in, test_name, test_matrix, test_matrix_nature):
    return test_matrix, test_matrix_nature


# Generates a signal game matrixes with payoffs in ascending order (1,2,3,4...)
# Runs a basic p2_choice and p1_deviations checks. 
def testA(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == False)

    print("[TestA-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_pool_action   == 1)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_pool_action   == 1)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestA-pool]: PASS")

# Semi decrement
def testB(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == False)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestB-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_pool_action   == 1)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_pool_action   == 1)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    print("[TestB-pool]: PASS")

# Full decrement
def testC(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == False)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestC-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_pool_action  == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_pool_action  == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    print("[TestC-pool]: PASS")


def testD(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    print("[TestD-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_pool_action  == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_pool_action  == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == False)

    print("[TestD-pool]: PASS")

def testE(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestE-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_pool_action  == 0)
    assert(parent_in.p2_pool_act_alt == 1)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_pool_action  == 1)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)
    assert(parent_in.solution_flag == True)

    print("[TestE-pool]: PASS")

def testF(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestF-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_pool_action  == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_pool_action  == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)
    assert(parent_in.eq_success    == False)

    print("[TestF-pool]: PASS")


def testG(parent_in, test_matrix, test_nature):
    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_REV, parent_in.WEK_HID)
    assert(parent_in.p2_top_choice == 0)
    assert(parent_in.p2_bot_choice == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    cl.seperating_eq(parent_in, test_matrix, parent_in.STR_HID, parent_in.WEK_REV)
    assert(parent_in.p2_top_choice == 1)
    assert(parent_in.p2_bot_choice == 1)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == True)  
    assert(parent_in.eq_success    == False)

    print("[TestG-sepr]: PASS")

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_REV, parent_in.WEK_REV)
    assert(parent_in.p2_pool_action  == 1)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == False)
    assert(parent_in.p1_bot_switch == False)  
    assert(parent_in.eq_success    == True)

    cl.pooling_eq(parent_in, test_matrix, test_nature, parent_in.STR_HID, parent_in.WEK_HID)
    assert(parent_in.p2_pool_action  == 0)
    assert(parent_in.p2_pool_act_alt == 0)
    assert(parent_in.p1_top_switch == True)
    assert(parent_in.p1_bot_switch == True)
    assert(parent_in.eq_success    == False)

    print("[TestG-pool]: PASS")

def testH(parent_in, test_matrix, test_nature):
    pass

def testI(parent_in, test_matrix, test_nature):
    pass

def testJ(parent_in, test_matrix, test_nature):
    pass

def testK(parent_in, test_matrix, test_nature):
    pass

def testL(parent_in, test_matrix, test_nature):
    pass

def testM(parent_in, test_matrix, test_nature):
    pass



test_functor_list = [testA, testB, testC, testD, testE, 
    testF, testG, testH, testI, testJ, testK, testL, testM]
testGEN_functor_list = [testA_gen, testB_gen, testC_gen, 
    testD_gen, testE_gen, testF_gen, testG_gen, testH_gen, 
    testI_gen, testJ_gen, testK_gen, testL_gen, testM_gen]

def gen_test_matricies_file(parent_in, tests_in):
    for i, test in enumerate(tests_in):
        test_name = "test" + test
        print("Gen"+test)
        test_matrix = np.zeros((4,2), dtype='i,i')
        test_matrix_nature = np.zeros((1,2))
        #testGEN_functor_list[i](parent_in, test_name, test_matrix, test_matrix_nature)
        tmtrx_out, tnatr_out = testGEN_functor_list[i](parent_in, test_name, test_matrix, test_matrix_nature)
        cn.import_matrix(parent_in, tmtrx_out, tnatr_out)
        cn.save_test_matrix(parent_in, test_name)