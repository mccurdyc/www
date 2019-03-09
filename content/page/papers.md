---
title: Published Papers
comments: false
---

# 2018

## Automatic detection and removal of ineffective mutants for the mutation analysis of relational database schemas

**McMinn, Phil and Wright, Chris and McCurdy, Colton and Kapfhammer, Gregory M.**

_Transactions on Software Engineering, 2018_

### Abstract

Data is one of an organization's most valuable and strategic assets. Testing the
relational database schema, which protects the integrity of this data, is of
paramount importance. Mutation analysis is a means of estimating the fault-finding
"strength" of a test suite. As with program mutation, however, relational database
schema mutation results in many ineffective mutants that both degrade test suite
quality estimates and make mutation analysis more time consuming. This paper presents
a taxonomy of ineffective mutants for relational database schemas, summarizing
the root causes of ineffectiveness with a series of key patterns evident in
database schemas. On the basis of these, we introduce algorithms that automatically
detect and remove ineffective mutants. In an experimental study involving the mutation
analysis of 34 schemas used with three popular relational database management
systems --- HyperSQL, PostgreSQL, and SQLite --- the results show that our algorithms
can identify and discard large numbers of ineffective mutants that can account
for up to 24% of mutants, leading to a change in mutation score for 33 out of 34
schemas. The tests for seven schemas were found to achieve 100% scores, indicating
that they were capable of detecting and killing all non-equivalent mutants.
The results also reveal that the execution cost of mutation analysis may be
significantly reduced, especially with "heavyweight" DBMSs like PostgreSQL.

### Resources


{{< download link="/papers/McMinn2018-paper.pdf" display="Paper" >}}

{{< repo-link "schemaanalyst/imdetect-replicate" >}}

{{< repo-link "schemaanalyst/schemaanalyst" >}}

---

# 2016

## mrstudyr: Retrospectively studying the effectiveness of mutant reduction techniques

**McCurdy, Colton J. and McMinn, Phil and Kapfhammer, Gregory M.**

_Proceedings of the 32nd International Conference on Software Maintenance and Evolution 2016, Raleigh, NC_

### Abstract

Mutation testing is a well-known method for measuring a test suite’s quality. However, due to its computational
expense and intrinsic difficulties (e.g., detecting equivalent mutants and potentially checking a mutant’s status
for each test), mutation testing is often challenging to practically use. To control the computational cost of
mutation testing, many reduction strategies have been proposed (e.g., uniform random sampling over mutants).
Yet, a stand-alone tool to compare the efficiency and effectiveness of these methods is heretofore unavailable.
Since existing mutation testing tools are often complex and language-dependent, this paper presents a tool, called
mrstudyr, that enables the "retrospective" study of mutant reduction methods using the data collected from a prior
analysis of all mutants. Focusing on the mutation operators and the mutants that they produce, the presented tool
allows developers to prototype and evaluate mutant reducers without being burdened by the implementation details
of mutation testing tools. Along with describing mrstudyr’s design and overviewing the experimental results from
using it, this paper inaugurates the public release of this open-source tool.

### Resources

{{< download link="/papers/icsme2016-mrstudyr.pdf" display="Paper" >}}

{{< repo-link "mccurdyc/mrstudyr" >}}


---

## SchemaAnalyst: Search-based test data generation for relational database schemas

**McMinn, Phil and Wright, Chris J. and Kinneer, Cody and McCurdy, Colton J. and Camara, Michael and Kapfhammer, Gregory M.**

_Proceedings of the 32nd International Conference on Software Maintenance and Evolution 2016, Raleigh, NC_

### Abstract

Data stored in relational databases plays a vital role in many aspects of society. When this data is incorrect, the
services that depend on it may be compromised. The database schema is the artefact responsible for maintaining the
integrity of stored data. Because of its critical function, the proper testing of the database schema is a task of
great importance. Employing a search-based approach to generate high-quality test data for database schemas,
SchemaAnalyst is a tool that supports testing this key software component. This presented tool is extensible
and includes both an evaluation framework for assessing the quality of the generated tests and full-featured
documentation. In addition to describing the design and implementation of SchemaAnalyst and overviewing its efficiency
and effectiveness, this paper coincides with the tool’s public release, thereby enhancing practitioners’ ability to
test relational database schemas.

### Resources

{{< download link="/papers/McMinn2016c-paper.pdf" display="Paper" >}}

{{< repo-link "schemaanalyst-team/schemaanalyst" >}}
