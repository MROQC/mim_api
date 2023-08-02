# MIM API to initiate workflows

#### Author: @nehabhomia

## Overview 
This is python code to interact with MIM assistant to initiate specified workflows on the given nids and source lists.

## Requirements

### 1. CSV file
It requires a CSV file as input. This csv file should have rows in the format of 3 variables - nid,workflow,source_list

### 2. Environment variables
It requires the environment variables of host and bearer token to interact through the API.

## Execution

### 1. Run main.py
Run main.py using the command
> python main.py <file_path>

where the file_path points to the csv file as outlined in Requirements #1

This will execute all the rules as outlined in the csv file.

### 2. For Testing or Debugging
To make individual api calls and/or interact with the api interface, run the mim_api.py file.
It will display terminal prompts and accept user input to execute a single API call.
