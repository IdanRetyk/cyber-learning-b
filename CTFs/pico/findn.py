target = anger = 13107399849270713206256942541790617196098315419037969103296263514322255692659

found = False
for n in range(1_000_000_00,1_000_000_000):
    if pow(anger,65537,n) == anger:
        print(n)
        found = True

print(f"{found =}")