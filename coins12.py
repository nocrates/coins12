'''
  12 coins problem solution

  Problem definition:

  Given 12 coins that are identical with the exception that 1 coin is either lighter or heavier
  than the others. Given a scale which only determines if one side is heavier than the other, or
  if the sides are balanced. Given the scale can only be used 3 times.
  What is the algorithm to find the special coin, as well as determine whether it is too light or too heavy.

  Note that in this code there are places where the last else is not necessary since we are returning values.
  Although it is a valid optimization, this has been left as is for readibility.
'''

# Some convenient labels
RIGHT_HEAVY = -1
LEFT_HEAVY = 1
BALANCED = 0

HEAVY = 1
LIGHT = -1

#######
# Measure two arrays of coins. A coin is an int representing it's weight
#  Adds up the weights on each side and compares the two sums
#  Returns either LEFT_HEAVY, RIGHT_HEAVY or BALANCED
#######

def measure(stack_left, stack_right):
    weight_left = 0
    weight_right = 0
    for coin in stack_left:
        weight_left = weight_left + coin
    for coin in stack_right:
        weight_right = weight_right + coin

    if weight_left < weight_right:
        return RIGHT_HEAVY

    elif weight_left > weight_right:
        return LEFT_HEAVY

    else:
        return BALANCED

#######
# solve
#   Given an array of 12 coins
# returns tuple
#   1. coin number
#   2. LIGHT or HEAVY
#
# Returns None, None if there is no solution
#######

def solve(coins):
    if len(coins) != 12:
        return (None, None)

    # Start by measuring 4 coins on each side
    m1 = measure(
        [coins[0], coins[1], coins[2], coins[3]],
        [coins[4], coins[5], coins[6], coins[7]]
    )

    if m1 == BALANCED:
        # 1, 2, 3, 4, 5, 6, 7, 8 are all the same
        # One of 9, 10, 11, 12 are either too light or too heavy
        # Weight 9, 10, 11 with 3 coins that are known to be the same
        m2 = measure(
            [coins[0], coins[1], coins[2]],
            [coins[8], coins[9], coins[10]]
        )

        if m2 == BALANCED:
            # 12th coin is special. Determine if it is too light or heavy by comparing to any other coin.
            m3 = measure(
                [coins[0]],
                [coins[11]]
            )

            if m3 == RIGHT_HEAVY:
                return (11, HEAVY)
            elif m3 == LEFT_HEAVY:
                return (11, LIGHT)
            else:
                return (None, None) # just for completeness. This will occur only if there are no special coins.

        elif m2 == LEFT_HEAVY:
            # 1, 2, 3, 4, 5, 6, 7, 8, 12 are all the same.
            # One of 9, 10, 11 is too light
            # Pick any of these two and compare
            m3 = measure(
                [coins[8]],
                [coins[9]]
            )
            if m3 == BALANCED:
                return (10, LIGHT)
            elif m3 == RIGHT_HEAVY:
                return (8, LIGHT)
            elif m3 == LEFT_HEAVY:
                return (9, LIGHT)

        elif m2 == RIGHT_HEAVY:
            # 1, 2, 3, 4, 5, 6, 7, 8, 12 are all the same.
            # One of 9, 10, 11 is too heavy
            # Pick any of these two and compare
            m3 = measure(
                [coins[8]],
                [coins[9]]
            )
            if m3 == RIGHT_HEAVY:
                return (9, HEAVY)
            elif m3 == LEFT_HEAVY:
                return (8, HEAVY)
            else:
                return (10, HEAVY)

    else:
        # 9, 10, 11, 12 are all the same.
        # Set aside 7 and 8
        # Move 3 coins from one side to the other
        m2 = measure(
            [coins[0], coins[1], coins[4]],
            [coins[2], coins[3], coins[5]]
        )

        if m2 == BALANCED:
            # 1, 2, 3, 4, 5, 6, 9, 10, 11, 12 are all the same.
            # One of 7 or 8 is too light or too heavy
            # if m1 is RIGHT_HEAVY, too heavy
            # if m1 is LEFT_HEAVY, too light
            # Compare one of the coins to a known good.
            m3 = measure(
                [coins[0]],
                [coins[6]]
            )
            if m3 == LEFT_HEAVY:
                return (6, LIGHT)
            elif m3 == RIGHT_HEAVY:
                return (6, HEAVY)
            else:
                return (7, HEAVY if m1 == RIGHT_HEAVY else LIGHT)

        elif m2 == m1:
            # Scales were same as first measurement
            # 3, 4, 5, 7, 8, 9, 10, 11, 12 are all the same
            # One of 1, 2, or 6 are either too light or too heavy
            # Compare 1, and 2
            m3 = measure(
                [coins[0]],
                [coins[1]]
            )
            if m3 == LEFT_HEAVY:
                if m2 == LEFT_HEAVY:
                    return (0, HEAVY)
                else:
                    return (1, LIGHT)
            elif m3 == RIGHT_HEAVY:
                if m2 == RIGHT_HEAVY:
                    return (0, LIGHT)
                else:
                    return (1, HEAVY)
            elif m3 == BALANCED:
                return (5, HEAVY if m1 == RIGHT_HEAVY else LIGHT)


        else:
            # Scales are opposite of first measurement
            # 1, 2, 6, 7, 8, 9, 10, 11, 12 are all the same
            # One of 3, 4, 5 are either too light or too heavy
            # Compare 3 and 4
            m3 = measure(
                [coins[2]],
                [coins[3]]
            )
            if m3 == RIGHT_HEAVY:
                if m2 == RIGHT_HEAVY:
                    return (3, HEAVY)
                else:
                    return (2, LIGHT)
            elif m3 == LEFT_HEAVY:
                if m2 == LEFT_HEAVY:
                    return (3, LIGHT)
                else:
                    return (2, HEAVY)
            elif m3 == BALANCED:
                return (4, HEAVY if m1 == RIGHT_HEAVY else LIGHT)


    return (None, None)


#######
#
# Test method
#
# Attempt every possible coin as either being too light or too heavy
#
#######
if __name__ == '__main__':
    test_coins = []
    for i in range(12):
        test_coins.append(0)


    # Try every combination
    for i in range(12):
        for alt_weight in [LIGHT, HEAVY]:
            test_coins[i] = alt_weight

            (coin_num, weight) = solve(test_coins)

            result_msg = ''
            if coin_num == i and alt_weight == weight:
                result_msg = 'Pass'
            elif coin_num == i:
                result_msg = 'Incorrect weight'
            else:
                result_msg = 'Incorrect coin'

            print '%d %s : %s' % (i+1, 'HEAVY' if alt_weight == HEAVY else 'LIGHT', result_msg)

        test_coins[i] = 0
