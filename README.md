# BDL API Wrapper

### Overview

This project is an API wrapper for accessing **Bank Danych Lokalnych: GUS**, Poland's largest database on the economy, society, and environment.

It provides access to thousands of statistical features organized thematically.

#### Guide

- You can retrieve detailed data by simply knowing the [`subject_id`](https://bdl.stat.gov.pl/bdl/dane/podgrup/temat#).<br> *Note:* `subject_id` *always looks like P####.*
- Once you query the API with a `subject_id`, different data categories will be displayed. Each category contains a unique `variable_id`.
- By using the `variable_id`, you can then access the specific data you're interested in.
