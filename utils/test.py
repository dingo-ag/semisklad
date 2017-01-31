# import csv
# import os
# from settings.base import BASE_DIR
#
# path = os.path.join(BASE_DIR, 'utils/phone_codes.csv')
#
# with open(path) as codes:
#     reader = csv.DictReader(codes)
#     for row in reader:
#         print(repr(row['code']), row['code'] == '67')
#         if row['code'] == '67':
#             district = row['operator_region']
#             print(district)
#             break
#
count = 1
for seq1 in range(10, 100):
    for seq2 in range(11, 100):
        if seq1 < seq2:
            nums1 = [int(i) for i in str(seq1)]
            nums2 = [int(i) for i in str(seq2)]

            if nums1[0] in nums2 and nums1[1] != 0 and nums2[not nums2.index(nums1[0])] != 0:
                if nums1[1]/nums2[not nums2.index(nums1[0])] == seq1/seq2:
                    count *= seq2 / seq1
                    print(seq1, seq2)
            if nums1[1] in nums2 and nums1[1] != 0 and nums2[not nums2.index(nums1[1])] != 0:
                if nums1[0] / nums2[not nums2.index(nums1[1])] == seq1 / seq2:
                    count *= seq2 / seq1
                    print(seq1, seq2)
print(count)





