import click
import yaml
from simphony.core.keywords import KEYWORDS


def generate_class_import():
    return [
        "from simphony.material_relations.material_relation import (\n",
        "\tMaterialRelation)\n",
        "from simphony.core.cuba import CUBA\n",
        "import simphony.core.data_container as dc\n",
        "\n",
        "\n",
    ]


def generate_class_header(mr):
    return [
        "class {MR_NAME}(MaterialRelation):\n".format(
            MR_NAME=mr['class_name']
        ),
        "\n"
    ]


def generate_description_block(mr):
    return [
        "\t\"\"\" Automatically generated implementation of the\n",
        "\t{MR_NAME} material-relation\n".format(
            MR_NAME=mr['class_name']
        ),
        "\n",
        "\tAttributes\n",
        "\t----------\n",
        "\n",
    ]


def generate_attributes_description(mr):

    code = []

    for param in mr['supported_parameters']:

        key = param['cuba'].split('.')[1]

        code += [
            "\t{ATT_NAME} : {ATT_TYPE}\n".format(
                ATT_NAME=KEYWORDS[key].name.lower(),
                ATT_TYPE=KEYWORDS[key].dtype
            ),
            "\t\t{ATT_DESC}\n".format(
                ATT_DESC=KEYWORDS[key].description
            ),
        ]

    return code


def generate_initializer(mr):

    code = []

    sub_param_cuba = ""

    code += [
        "\n\t\"\"\"\n",
        "\n",
        "\tdef __init(\n",
        "\t\tself,\n",
        "\t\tmaterials",
    ]

    for param in mr['supported_parameters']:

        sub_param_cuba += "\n\t\t\t\t"+param['cuba']+","

        code += [
            ",\n",
            "\t\t{ATT_NAME}".format(
                ATT_NAME=param['cuba'].split('.')[1].lower()
            ),
        ]

    code += [
        "\n\t):\n",
        "\t\tsuper({MR_NAME}, self).__init__(\n".format(
            MR_NAME=mr['class_name']
        ),
        "\t\t\tname=\"{MR_NAME}\",\n".format(MR_NAME=mr['class_name']),
        "\t\t\tdescription=\"{MR_DESC}\",  # noqa\n".format(
            MR_DESC=mr['description']
        ),
        "\t\t\tparameters=dc.DataContainer(),\n",
        "\t\t\tsupported_parameters=[{MR_S_PARAM}\n\t\t\t],".format(
            MR_S_PARAM=sub_param_cuba
        ),
        "\n",
        "\t\t\tmaterials=materials,\n",
        "\t\t\tnum_materials={MR_MATS},\n".format(
            MR_MATS=mr['allowed_number_materials']
        ),
        "\t\t\tkind={MR_KIND}\n".format(MR_KIND=mr['kind']),
        "\t\t)\n",
        "\n",
    ]

    return code


def generate_property_get_set(mr):

    getter_string = ""
    getter_string += "\t@property\n"
    getter_string += "\tdef {PROP_NAME}(self):\n"
    getter_string += "\t\treturn self.parameters[{CUBA_KEY}]\n"

    setter_string = ""
    setter_string += "\t@{PROP_NAME}.setter\n"
    setter_string += "\tdef {PROP_NAME}(self, value):\n"
    setter_string += "\t\tself.parameters[{CUBA_KEY}] = value\n"

    get_set_block = getter_string + "\n" + setter_string + "\n"

    code = ""

    for param in mr['supported_parameters']:

        code += get_set_block.format(
            PROP_NAME=param['cuba'].split('.')[1].lower(),
            CUBA_KEY=param['cuba']
        )

    return code


@click.group()
def cli():
    """ Auto-generate code from material-relation yaml description. """


@cli.command()
@click.argument('input', type=click.File('rb'))
@click.argument('outpath', type=click.Path(exists=True))
def python(input, outpath):
    """ Create the material-relation class.
    """
    material_relations = yaml.safe_load(input)

    for mr in material_relations:
        with open(outpath+mr['class_name']+'.py', 'w+') as mrFile:
            lines = []
            lines += generate_class_import()
            lines += generate_class_header(mr)
            lines += generate_description_block(mr)
            lines += generate_attributes_description(mr)
            lines += generate_initializer(mr)
            lines += generate_property_get_set(mr)

            mrFile.writelines([i.replace('\t', '    ') for i in lines])


@cli.command()
@click.argument('input', type=click.File('rb'))
@click.argument('outpath', type=click.Path(exists=True))
def test(input, outpath):
    pass

if __name__ == '__main__':
    cli()
