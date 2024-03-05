def file_handler(name,mode = "r",txt="",line=""):
    if name == "help":
        try:
            with open("help.txt","r") as file:
                return(file.read())
        except:
            return "ERR => can't open help."
    
    else:
        try:
            if mode == 'l':
                final_list = []
                with open(name,"r") as file:
                    get_list = file.readlines()
                    for i in get_list:
                        if i.endswith('\n'):
                            final_list.append(i[:-1])
                        else:
                            final_list.append(i)
                return final_list
            
            else:
                fl = open(name,mode)
                if mode == "r" or mode == "rb":
                    if line == "":
                        return fl.read()
                    else:
                        try:
                            if type(line) == int and line == 0:
                                return fl.readlines()
                            
                            elif type(line) == int and line > 0:
                                all_lines =  fl.readlines()
                                try:
                                    selected = all_lines[line-1]
                                except IndexError:
                                    selected = "null"
                                if selected.endswith('\n'):
                                    return selected[:-1]
                                else:
                                    return selected
                            elif type(line) == list:
                                result = []
                                all_lines =  fl.readlines()
                                corr_lines = []
                                try:
                                    for item in line:
                                        item = int(item)
                                        if item == 0:
                                            raise ZeroDivisionError("zde")
                                        corr_lines.append(item)
                                    
                                    for line_num in corr_lines:
                                        try:
                                            selected = all_lines[line_num-1]
                                        except IndexError:
                                            selected = f"null-{line_num}"
                                        if selected.endswith('\n'):
                                            selected = selected[:-1]
                                        result.append(selected)

                                    return result
                                
                                except ValueError:
                                    return "ERR: lines must be numbers and "
                                
                                except ZeroDivisionError:
                                    return "ERR: you can't use 0 in list "
                                                    
                                except:
                                    return "ERR: unkmown_2!"

                            else:
                                return ("InputError => can't find line.")
                        
                        except:
                                return "ERR => line must be a number."
                
                elif mode == "w" or mode == "wb":
                    try:
                        fl.write(txt)
                        return name
                    except:
                        raise Exception('error in writing file; mode = w,wb')
                    
                elif mode == "a" or mode == "a+":
                    try:
                        fl.write(txt)
                        return name
                    except:
                        raise Exception('error in writing file; mode = a,a+')
                    
                else:
                    return "InputErr => the availble modes now are ['r','w','a','a+','rb','wb'] "
            
        except FileNotFoundError:
            return "FileNotFoundError"
        except:
            return "ERR => unknown_1!"
        
        finally:
            try:
                fl.close()
            except:
                pass
