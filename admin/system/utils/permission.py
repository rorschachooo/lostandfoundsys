import operator

class PermissionUtil:
    def get_tree_permissions(all):
        parentList = [permission for permission in all if permission['type'] == 1 or (permission['type'] == 2 and permission['p_id'] == None)]
        # Traverse the first-level menu list and add the corresponding second-level menu to the children attribute of the first-level menu
        for permission in parentList:
            pid = permission['id']
            level2List = [permission1 for permission1 in all if permission1['p_id'] == pid]
            permission['children'] = level2List
            # Sort the first-level menu list and return the result
        return sorted(parentList, key=operator.itemgetter('orders'))

    def children_tree(pid, all_data):
        children_list = []
        for permission in all_data:
            if permission.get('p_id') == pid:
                children = PermissionUtil.children_tree(permission.get('id'), all_data)  # Recursive calls
                permission['children'] = children
                children_list.append(permission)
        return children_list