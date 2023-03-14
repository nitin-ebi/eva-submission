#!/bin/bash

set -Eeuo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SOURCE_DIR="$(dirname $(dirname $SCRIPT_DIR))/eva_submission/nextflow"

cwd=${PWD}
cd ${SCRIPT_DIR}

printf "\e[32m===== VALIDATION PIPELINE =====\e[0m\n"
nextflow run "${SOURCE_DIR}/validation.nf" -params-file test_validation_config.yaml

ls output/sv_check/test1_sv_check.log \
output/sv_check/test1_sv_list.vcf.gz \
output/assembly_check/test1.vcf.assembly_check.log \
output/assembly_check/test1.vcf.text_assembly_report \
output/assembly_check/test1.vcf.valid_assembly_report \
output/normalised_vcfs/test1.vcf.gz \
output/normalised_vcfs/test1.vcf_bcftools_norm.log

# clean up
rm -rf work .nextflow*
rm -r output
cd ${cwd}
