"""
How to use
Analyze Jira workflows to find specific class usage. The input file should be jiraworkflows table dump. An example SQL command to export only active workflows:
select * from jiraworkflows where workflowname in (select workflowname from jiraworkflows where workflowname in (select distinct workflow from workflowschemeentity));

How to run it
python3 wfconversion.py -w <nome do teu arquivo extraído pela banco>.csv -ac jsu -f csv -o workflowsjsu

Need to execute once for each app (com.onresolve.jira.groovy, com.googlecode.jsu, com.innovalog.jmwe)

Code below
"""

#!/usr/bin/env python3

import argparse
import copy
import csv
import json
import os
import sys
import xml.etree.ElementTree

# Increase CSV field size limit
csv.field_size_limit(sys.maxsize)

argparse = argparse.ArgumentParser(
    description="""
Analyze Jira workflows to find specific class usage. The input file should be `jiraworkflows` table dump. An example
SQL command to export only active workflows: select * from jiraworkflows where workflowname in (select workflowname
from jiraworkflows where workflowname in (select distinct workflow from workflowschemeentity));
"""
)
argparse.add_argument("-w", "--workflows", help="CSV file with workflows", required=True)
argparse.add_argument("-ac", "--app_class", help="Class/text to search in workflows", required=True)
argparse.add_argument("-f", "--format", help="Output format", choices=["json", "plain", "pretty", "csv"], default="csv")
argparse.add_argument(
    "-o", "--output", help="Output file for JSON or CSV formats. Stdout by default", default=sys.stdout
)
argparse.add_argument(
    "-e", "--export", action="store_true", default=False, help="Export each workflow into a separate XML file"
)
args = argparse.parse_args()

def safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")

def save_workflow(file_name, data):
    with open(file_name, "w", newline="", encoding="utf-8") as write_file:
        write_file.write(data)

def find_match_children(tree, path, text):
    ret_data = []
    for i in tree.findall(path):
        for el in i.findall(".//arg[@name='class.name']"):
            if text in el.text:
                attr = os.linesep.join(
                    sorted(
                        [
                            f"{elem.attrib['name']} = {elem.text}"
                            for elem in i.iter()
                            if elem is not i and elem.attrib["name"] not in ("class.name", "full.module.key")
                        ]
                    )
                )
                ret_data.append(os.linesep.join([f"class.name = {el.text}", attr]))
    return ret_data

def _process(save: bool = False):
    with open(args.workflows, "r", encoding="utf-8-sig", newline="") as f:
        next(f)
        reader = csv.DictReader(f, ["id", "workflowname", "creatorname", "descriptor", "islocked"])
        for r in reader:
            wf_name = r["workflowname"]
            if save:
                filename = safe_filename(f"{r['id']}_{wf_name}") + ".xml"
                save_workflow(filename, r["descriptor"])
            wfd = xml.etree.ElementTree.fromstring(r["descriptor"])
            wf = {wf_name: []}
            actions = {}
            for action in wfd.findall(".//*action"):
                catch = False
                action_name = f"{action.get('name')} ({action.get('id')})"
                transition = {}
                validators = find_match_children(action, ".//validators/validator", app)
                if len(validators) > 0:
                    transition["validators"] = validators
                    catch = True
                conditions = find_match_children(action, ".//restrict-to/conditions/condition", app)
                if len(conditions) > 0:
                    transition["conditions"] = conditions
                    catch = True
                post_functions = find_match_children(
                    action, ".//results/unconditional-result/post-functions/function", app
                )
                if len(post_functions) > 0:
                    transition["post-functions"] = post_functions
                    catch = True
                if catch:
                    actions[action_name] = transition
            wf[wf_name].append(actions)
            for c in copy.deepcopy(wf):
                if len(wf[c][0]) == 0:
                    del wf[c]
            if len(list(wf.keys())) > 0:
                workflows.append(wf)

def _output(of):
    if of == "json":
        if type(args.output) == str:
            ouf = open(f"{args.output}.{of}", mode="w", newline="", encoding="utf-8")
            json.dump(workflows, ouf)
        else:
            print(json.dumps(workflows))
    elif of == "pretty":
        print(json.dumps(workflows, indent=2))
    elif of == "plain":
        print("Workflow\\tTransition\\tType\\tClass")
        for wf in workflows:
            for ac in wf:
                line = f"{ac}"
                for ai, a in enumerate(wf[ac]):
                    if ai > 0:
                        line = "\\t"
                    for fi, f in enumerate(a):
                        line += f"\\t{f}"
                        for ii, i in enumerate(a[f]):
                            line += f"\\t{i}" if ii == 0 else f"\\t\\t{i}"
                            for ji, j in enumerate(a[f][i]):
                                line += f"\\t{j}" if ji == 0 else f"\\t\\t\\t{j}"
                                print(line)
                                line = ""
    elif of == "csv":
        headers = ["Workflow", "Transition", "Type", "Class", "Notes"]
        if type(args.output) == str:
            ouf = open(f"{args.output}.{of}", mode="w", newline="", encoding="utf-8")
        else:
            ouf = args.output
        writer = csv.DictWriter(ouf, fieldnames=headers)
        writer.writeheader()
        for wf in workflows:
            for ac in wf:
                line = {"Workflow": ac}
                for a in wf[ac]:
                    for f in a:
                        line["Transition"] = f
                        for i in a[f]:
                            line["Type"] = i
                            for j in a[f][i]:
                                line["Class"] = j
                                writer.writerow(line)
                                line = {}

app = args.app_class
workflows = []

_process(args.export)
_output(args.format)
