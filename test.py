
def openLock(deadends: list[str], target: str) -> int:
        # BFS

        visited = [False for _ in range(10000)]

        for dd in deadends:
            visited[int(dd)] = True
        
        count = -1
        curr = ["0000"]
        while len(curr) > 0:
            count += 1
            
                
            next = []
            for code in curr:
                curr.pop(0)
                if not visited[int(code)]:
                    
                    if len(curr) < 185 and count > 5:
                        pass
                    
                    
                    if int(code) == int(target):
                        return count
                    
                    visited[int(code)] = True

                    # Get reachable codes from current code

                    if code[0] == '9':
                        next.append('0' + code[1:])
                        next.append('8' + code[1:])
                    elif code[0] == '0':
                        next.append('1' + code[1:])
                        next.append('9' + code[1:])
                    else:
                        next.append(str(int(code[0]) + 1)  + code[1:])
                        next.append(str(int(code[0]) - 1) + code[1:])
                    
                    if code[1] == '9':
                        next.append(code[0] + '0' + code[2:])
                        next.append(code[0] + '8' + code[2:])
                    elif code[1] == '0':
                        next.append(code[0] + '1' + code[2:])
                        next.append(code[0] + '9' + code[2:])
                    else:
                        next.append(code[0] + str(int(code[1]) + 1)  + code[2:])
                        next.append(code[0] + str(int(code[1]) - 1)  + code[2:])
                    
                    if code[2] == '9':
                        next.append(code[:2] + '0' + code[3])
                        next.append(code[:2] + '8' + code[3])
                    elif code[2] == '0':
                        next.append(code[:2] + '1' + code[3])
                        next.append(code[:2] + '9' + code[3])
                    else:
                        next.append(code[:2] + str(int(code[1]) + 1)  + code[3])
                        next.append(code[:2] + str(int(code[1]) - 1)  + code[3])
                    
                    if code[3] == '9':
                        next.append(code[:3] + '0')
                        next.append(code[:3] + '8')
                    elif code[3] == '0':
                        next.append(code[:3] + '1')
                        next.append(code[:3] + '9')
                    else:
                        next.append(str(int(code) + 1).zfill(4))
                        next.append(str(int(code) - 1).zfill(4))

                
            curr = next


        return -1


s = "- (3 + (4 + 5))"
print(openLock(["0201","0101","0102","1212","2002"],"0202"))