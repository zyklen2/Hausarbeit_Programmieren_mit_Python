# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 17:14:36 2022

@author: Oliver
"""

import unittest
import numpy as np
from helper import Helper

class Helpertests(unittest.TestCase):
    
    test_list1 = np.array([1, 6, 8, 3, 7, 7, 5, 3, 6, 3, 5, 7, 1, 2, 8, 6, 2, 9, 3, 9])
    test_list2 = np.array([5, 7, 5, 3, 8, 4, 0, 8, 1, 3, 5, 1, 8, 8, 9, 3, 6, 6, 5, 6])
    test_list3 = np.array([3, 1, 8, 9, 6, 0, 6, 4, 1, 4, 6, 3, 4, 2, 2, 9, 8, 9, 0, 1])
    test_list4 = np.array([3, 9, 3, 4, 1, 3, 9, 5, 7, 4, 7, 8, 5, 2, 9, 8, 7, 3, 8, 3])
    float_test_list1 = np.array([1.6728881716804118, 1.8107490427303061, 1.628285476091837, 1.6807207458735007, 1.8511917088654195, 
                                 1.6650946067873689, 1.7602190488045713, 1.6165582345002754, 1.8415155980377587, 1.6762840250275353, 
                                 1.5377326794538162, 1.706515920275895, 1.5249177016257254, 1.5359709382040059, 1.7641168243666583, 
                                 1.544934872248788, 1.5598217028041403, 1.6043907469568746, 1.6145889757348606, 1.8094675491186658])
    float_test_list2 = np.array([1.7275331320864151, 1.762887861996341, 1.884239408229998, 1.6717862144634847, 1.888883707468039, 
                                 1.8876017334790074, 1.5337510718696528, 1.575100701148494, 1.595410381799891, 1.8348706834530042, 
                                 1.648386778332705, 1.547031849361123, 1.8630331319755413, 1.877933714250627, 1.5592825305726425, 
                                 1.881626180040263, 1.6530665586322904, 1.7706957025121, 1.6869118345855376, 1.830668073343049])
    float_test_list3 = np.array([1.8314146532485158, 1.6661844624551183, 1.8406983008908764, 1.528272661740465, 1.6723523697979807, 
                                 1.5830707593846007, 1.8662255308832674, 1.7502158265356433, 1.8860807946322296, 1.5900598445639915, 
                                 1.5815806175301517, 1.6896940727314573, 1.8640763963654048, 1.8809930500050835, 1.8798218819574974, 
                                 1.7143442130827047, 1.5901954788162456, 1.616402670095347, 1.8650605912072948, 1.6202190757211805])
    float_test_list4 = np.array([1.646660331903733, 1.819283481182488, 1.5365337283517126, 1.5997645645091558, 1.8224159417863568, 
                                 1.5330355499058193, 1.5983771831724345, 1.715140322502946, 1.6465769394558214, 1.7258694331317168, 
                                 1.83170485928881, 1.8020695218474982, 1.794141653895371, 1.5354548599381106, 1.8068236528813713, 
                                 1.540806817663896, 1.7112735475779077, 1.5148406904800533, 1.659073206247792, 1.7486094090980415])
    
    def test_calculate_squared_difference(self):
        helper_obj = Helper()
        self.assertEqual(helper_obj.calculate_squared_difference(self.test_list1, self.test_list2), 280)
        self.assertEqual(helper_obj.calculate_squared_difference(self.test_list2, self.test_list3), 363)
        self.assertEqual(helper_obj.calculate_squared_difference(self.test_list3, self.test_list4), 376)
        self.assertEqual(helper_obj.calculate_squared_difference(self.test_list4, self.test_list1), 261)
    
        self.assertEqual(helper_obj.calculate_squared_difference(self.float_test_list1, self.float_test_list2), 0.7268132981665956)
        self.assertEqual(helper_obj.calculate_squared_difference(self.float_test_list2, self.float_test_list3), 0.7272256548156935)
        self.assertEqual(helper_obj.calculate_squared_difference(self.float_test_list3, self.float_test_list4), 0.6478140861526255)
        self.assertEqual(helper_obj.calculate_squared_difference(self.float_test_list4, self.float_test_list1), 0.3168839568724078)
        return
    
    def test_sort_multiple_arrays(self):
        helper_obj = Helper()
        result1 = [5, 8, 6, 8, 5, 8, 3, 3, 5, 0, 1, 3, 7, 4, 8, 1, 5, 9, 6, 6]
        self.assertTrue(all([val == result1[nr] for nr, val in enumerate(helper_obj.sort_multiple_arrays([self.test_list1, self.test_list2])[1])]))
        result2 = [6, 3, 1, 4, 9, 9, 0, 6, 0, 3, 8, 8, 9, 1, 1, 6, 4, 2, 4, 2]
        self.assertTrue(all([val == result2[nr] for nr, val in enumerate(helper_obj.sort_multiple_arrays([self.test_list2, self.test_list3])[1])]))
        result3 = [3, 8, 3, 9, 7, 9, 2, 8, 3, 5, 5, 4, 9, 7, 1, 3, 7, 4, 8, 3]
        self.assertTrue(all([val == result3[nr] for nr, val in enumerate(helper_obj.sort_multiple_arrays([self.test_list3, self.test_list4])[1])]))
        result4 = [7, 2, 1, 9, 7, 9, 8, 3, 3, 3, 1, 6, 5, 2, 3, 7, 6, 5, 8, 6]
        self.assertTrue(all([val == result4[nr] for nr, val in enumerate(helper_obj.sort_multiple_arrays([self.test_list4, self.test_list1])[1])]))
    
        float_result1 = [1.8630331319755413, 1.877933714250627, 1.648386778332705, 1.881626180040263, 1.6530665586322904, 
                         1.7706957025121, 1.6869118345855376, 1.575100701148494, 1.884239408229998, 1.8876017334790074, 
                         1.7275331320864151, 1.8348706834530042, 1.6717862144634847, 1.547031849361123, 1.5337510718696528, 
                         1.5592825305726425, 1.830668073343049, 1.762887861996341, 1.595410381799891, 1.888883707468039]
        self.assertTrue(all([val == float_result1[nr] for nr, val in enumerate(helper_obj.sort_multiple_arrays([self.float_test_list1, self.float_test_list2])[1])]))
        float_result2 = [1.8662255308832674, 1.6896940727314573, 1.8798218819574974, 1.7502158265356433, 1.8860807946322296, 
                         1.5815806175301517, 1.5901954788162456, 1.528272661740465, 1.8650605912072948, 1.8314146532485158, 
                         1.6661844624551183, 1.616402670095347, 1.6202190757211805, 1.5900598445639915, 1.8640763963654048, 
                         1.8809930500050835, 1.7143442130827047, 1.8406983008908764, 1.5830707593846007, 1.6723523697979807]
        self.assertTrue(all([val == float_result2[nr] for nr, val in enumerate(helper_obj.sort_multiple_arrays([self.float_test_list2, self.float_test_list3])[1])]))
        float_result3 = [1.5997645645091558, 1.83170485928881, 1.5330355499058193, 1.7258694331317168, 1.7112735475779077, 
                         1.5148406904800533, 1.7486094090980415, 1.819283481182488, 1.8224159417863568, 1.8020695218474982, 
                         1.540806817663896, 1.715140322502946, 1.646660331903733, 1.5365337283517126, 1.794141653895371, 
                         1.659073206247792, 1.5983771831724345, 1.8068236528813713, 1.5354548599381106, 1.6465769394558214]
        self.assertTrue(all([val == float_result3[nr] for nr, val in enumerate(helper_obj.sort_multiple_arrays([self.float_test_list3, self.float_test_list4])[1])]))
        float_result4 = [1.6043907469568746, 1.6650946067873689, 1.5359709382040059, 1.628285476091837, 1.544934872248788, 
                         1.7602190488045713, 1.6807207458735007, 1.8415155980377587, 1.6728881716804118, 1.6145889757348606, 
                         1.5598217028041403, 1.6165582345002754, 1.6762840250275353, 1.8094675491186658, 1.5249177016257254, 
                         1.706515920275895, 1.7641168243666583, 1.8107490427303061, 1.8511917088654195, 1.5377326794538162]
        self.assertTrue(all([val == float_result4[nr] for nr, val in enumerate(helper_obj.sort_multiple_arrays([self.float_test_list4, self.float_test_list1])[1])]))
        return
    
if __name__ == '__main__':
    unittest.main()