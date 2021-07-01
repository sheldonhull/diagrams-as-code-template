from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECS, Fargate, EC2
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, InternetGateway
from diagrams.aws.security import WAF
from diagrams.onprem.compute import Server

# Add argument and path packages to help with passing in arguments via command line
import argparse, sys, os
from pathlib import Path


def main():
    # Simplify optional argument parsing with a coalesce function
    def coalesce(*arg):
        for el in arg:
            if el is not None:
                return el
        return None

    # Generate a line by providing the nodes to connect in a list.
    # Style the lines and color to make it easier to trace several different paths on the same graph
    def colored_flow(nodes, color="black", style="", label=""):
        print(f"==> def colored_flow: nodes {nodes}")
        for index, n2 in zip(nodes, nodes[1:]):
            print(f"\t----> {index.label} >> Edge(label={label}) >> {n2.label}")
            (
                index
                >> Edge(label=label, style=style)
                >> Edge(color=color, style=style)
                >> n2
            )
        print("completed with colored_flow")

    ############################################
    # Attributes (LOTS OF EXPERIMINATION HERE) #
    ############################################

    graph_attr = {
        "imagescale": "true",  # true | false | width | height | both
        "fixedsize": "true",  # true | false
        "fontsize": "45",
        "remindcross": "true",
        # "bgcolor": "transparent",
        "bgcolor": "white",
        # "splines": "polyline",
        # "splines": "lines",
        "splines": "splines",
        # "splines": "ortho",
        # "splines": "curved",
        # "splines": "curved",
        # "splines": "compound",
        # "splines": "true",
        "overlap": "false",
        "arrowsize": "10",
        "penwidth": "3",
        # "penwidth": "0",
        # "width": "0.8",
        # "height": "0.8",
        "ratio": "compress",
        # "labeldistance":"10.0",
        "overlap": "scale",
        "overlap_shrink": "true",
        "labelloc": "b",
        "concentrate": "true",
        # "repulsiveforce": "10.0",
        # "rankdir": "LR",
        # "color": "darkblue",
        # "labelfontsize": "18.0",
        # "labelloc":"c",
        # "labelfloat": "false",
        # "layout":"neato",
        # "layout":"fdp",
        # "pack": "true",
    }

    ################################
    # PARSE COMMAND LINE ARGUMENTS #
    ################################

    cwd = Path.cwd()
    # abs_cwd = cwd.parent.absolute()
    # project_directory = os.path.dirname(abs_cwd)
    # project_directory = os.path.dirname(cwd)
    project_directory = Path.cwd()
    print(f"project_directory       : {project_directory}")
    artifact_directory = os.path.join(project_directory, "artifacts")
    # os.Mkdir(artifact_directory,0o777)

    print(f"artifact_directory      : {artifact_directory}")

    parser = argparse.ArgumentParser()
    parser.add_argument("--title", help="title for the diagram")
    parser.add_argument(
        "--filename", help="output file name. Do not include the extension"
    )
    parser.add_argument("--outformat", help="default png")

    args = parser.parse_args()
    outformat = coalesce(args.outformat, "png")
    title = coalesce(args.title, "Diagram")

    print(f"title     : {title}")
    filename = os.path.join(
        artifact_directory,
        coalesce(args.filename, "diagram-simple"),  # exclude file extension on this one
    )
    filenamegraph = os.path.join(
        artifact_directory, coalesce(args.filename, "diagram-simple.gv")
    )
    print(f"outformat     : {outformat}")
    print(f"filename      : {filename}")
    print(f"filenamegraph : {filenamegraph}")

    #######################################################
    # Setup Some Input Variables for Easier Customization #
    #######################################################
    title = title
    show = True
    direction = "LR"
    smaller = "0.8"

    with Diagram(
        name=title,
        direction=direction,
        show=show,
        graph_attr=graph_attr,
        filename=filename,
        outformat=outformat,
    ) as diag:
        # Non Clustered
        waf = WAF("waf")
        user = Server("user")

        # Cluster = Group, so this outline will group all the items nested in it automatically
        with Cluster("vpc"):
            igw_gateway = InternetGateway("igw")

            # Subcluster for grouping inside the vpc
            with Cluster("subnets_public"):
                ec2_server_web_server = EC2("web_server")
            # Another subcluster equal to the subnet one above it
            with Cluster("subnets_private"):
                ec2_server_app_server = EC2("app_server")
                ec2_server_image_processing = EC2("async_image_processing")

        # Now I document the flow here for clarity
        # Could do it in each node area, but I like the "connection flow" to be at the bottom
        ###################################################
        # FLOW OF ACTION, NETWORK, or OTHER PATH TO CHART #
        ###################################################
        # NOTE: This could be done manually without colored flow, but I like the readability of using a function
        # user >> waf >> igw_gateway >> ec2_server_web_server >> ec2_server_app_server >> ec2_server_image_processing

        colored_flow(
            nodes=(
                user,
                waf,
                igw_gateway,
                ec2_server_web_server,
                ec2_server_app_server,
                ec2_server_image_processing,
            ),
            color="darkblue",
            style="dashed,setlinewidth(5)",
        )

    diag


if __name__ == "__main__":
    # execute only if run as a script
    main()
