

def LoadMap(file_path):
    if file_path is None:
        print("FILE ERROR! File is None!")
        return [0, 0]
    elif len(file_path) == 0:
        print("FILE ERROR! File lenght is 0!")
        return [0, 0]

    with open(file_path) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

        all_list = []
        param_list = []

        for element in content:
            element_list = element.split()

            if element_list[0][0] != '#':

                element_type = GetElementType(element_list)

                PrintElementDebug(element_list)

                if element[0][0] != '[':
                    all_list.append([element_type ,element_list])
                else:
                    param_list.append(element)
        
        return [all_list, param_list]

def PrintElementDebug(element):
    if element[0][0] != '[':
        if element[1] == "WorldRectangleRigid":
            print("DEBUG: |ID: {0}|TYPE: {1}|GROUP: {2}|POSITION: x={3} y={4}| SIZE: width={5} height={6}|".format(
                        element[0], element[1], element[2], element[3],
                        element[4], element[5], element[6]
                    )
                    )
        elif element[1] == "MetalCrate":
            print("DEBUG: |ID: {0}|TYPE: {1}|GROUP: {2}|POSITION: x={3} y={4}|".format(
                        element[0], element[1], element[2], element[3],
                        element[4]
                    )
                    )
        elif element[1] == "WorldRectangleSensor":
            print("DEBUG: |ID: {0}|TYPE: {1}|GROUP: {2}|POSITION: x={3} y={4}| SIZE: width={5} height={6}|LAYER: {7}|".format(
                        element[0], element[1], element[2], element[3],
                        element[4], element[5], element[6], element[7]
                    )
                    )
        elif element[1] == "FireLight" or element[1] == "LightSource":
            if len(element) > 8:
                print("DEBUG: |ID: {0}|TYPE: {1}|GROUP: {2}|POSITION: x={3} y={4}| POWER: width={5}| LIGHT FORM={6}|LAYER: {7}| COLOR PRESET: {8}|".format(
                        element[0], element[1], element[2], element[3],
                        element[4], element[5], element[6], element[7], element[8]
                    )
                    )
            else:
                print("DEBUG: |ID: {0}|TYPE: {1}|GROUP: {2}|POSITION: x={3} y={4}| POWER: width={5}| LIGHT FORM={6}|LAYER: {7}|".format(
                        element[0], element[1], element[2], element[3],
                        element[4], element[5], element[6], element[7]
                    )
                    )
# 1 - WorldRectangleRigid
# 2 - MetalCrate
# 3 - WorldRectangleSensor
# 4 - Light
# 0 - ERROR
def GetElementType(element):
    if element[0][0] != '[':
        if element[1] == "WorldRectangleRigid":
            return 1
        elif element[1] == "MetalCrate":
            return 2
        elif element[1] == "WorldRectangleSensor":
            return 3
        elif element[1] == "FireLight" or element[1] == "LightSource":
            return 4
    return 0
            