import random

def divide_teams_into_pools(teams, num_pools):
    # Shuffle the teams randomly
    random.shuffle(teams)
    

    print(num_pools)
    # Initialize pools
    pools = [[] for _ in range(num_pools)]

    print(pools)
    
    # Distribute teams into pools
    for team in teams:
        # Find the pool with the fewest teams
        min_pool = min(pools, key=len)
        min_pool.append(team)
    
    return pools

def main():
    # Example usage
    num_teams = int(input("How many teams do you have? "))
    teams = [input(f"Enter team {i+1} name: ") for i in range(num_teams)]
    
    num_pools = int(input("How many pools do you want? "))
    pools = divide_teams_into_pools(teams, num_pools)
    
    # Print the pools
    for i, pool in enumerate(pools, start=1):
        print(f"Pool {i}: {', '.join(pool)}")

if __name__ == "__main__":
    main()