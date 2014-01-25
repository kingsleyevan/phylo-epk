#!/usr/bin/env python


import random
from short_read_analysis import variant_detection

def bootstrap_vcf(vcfobj,samplenum,outbase):
    
    '''Randomly sample items of the vcfobj dictionary (created by variant_detection.loadvcf) 
    	samplenum times and write smartpca files with write_smartpca_genotypes
     '''
    
    for x in xrange(samplenum):
    	vcfsamp = {}
	for i in xrange(len(vcfobj)):
            vcfsamp[('Btstrpsite', str(i))] = random.choice(vcfobj.values())	
	
	current_outbase = '%s_%s' % (outbase,str(x))
	variant_detection.write_smartpca_genotypes(vcfsamp, current_outbase)

	print "wrote %s" % x

import subprocess

def smartpca_batch(directory):

    ''' Run smartpca on every .par file in the directory, then
    	run twstats on each resulting .eval file.'''

    subprocess.call('for f in %s*.par; do smartpca -p $f; done') % directory
    subprocess.call('for f in %s*.eval; do twstats -t twtable -i $f -o $f.twstats; done') % directory

