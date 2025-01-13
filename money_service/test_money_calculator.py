from money_calculator import calculate_minimal_transfers

def test_money_calculator():
    t1 = {'a': 10000, 'b': -1000, 'c': -3000, 'd': -2000 , 'e': -6000, 'f': 2000, 'g': -1500, 'h':1500}
    #print(calculate_minimal_transfers(t1))
    t2 = {'갓갓갓갓갓갓, 니카': -31600, '지갑타노스': 126500, '제발 주세요, 스키장 복구 -30': 195100, '원화콜렉터_구조반, 현금청소기': -100000, '블러핑으로 다땀, 저 풀하우스요': -170000, 'A형독감': -20000}
    print(calculate_minimal_transfers(t2))
test_money_calculator()