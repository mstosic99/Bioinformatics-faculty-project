# -*- coding: utf-8 -*-
"""Bioinformatika projekat 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xuRHcp7Xz5XA5_-ureqUP7XM92ho7Hrb
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Projekat 2 - 20 bodova

Dati su FASTQ fajlovi koji su rezultat sekvenciranja dela exoma koji se nalazi na hromozomu 11 (podaci su uzeti iz uzoraka 1000 Genomes projekta).
(tabela sa imenom uzoraka koji je dodeljen svakom studentu je data u fajlu Lista zadataka 2 2021).

### Rok za predaju je 3. Jun, do kraja dana.
Do datog roka je potrebno poslati rezultate emailom, na adresu grakocevic@raf.rs.

Kao rezultat projekta se potrebno je predati:  
1. Kod kojim su generisani rezultati (ipynb ili python skripta)
2. Kraći izveštaj sa tekstualnim odgovorima na pitanja i grafikonima **u PDF formatu**

Projekat je moguće raditi pojedinačno ili u paru. **Ukoliko se projekat radi u paru, svaki student predaje i brani projekat posebno, uz napomenu da je projekat urađen u paru; pri tome svaki student treba da obradi podatke iz eksperimenta koji mu dodeljen, a rad u paru se odnosi na programski kod i šablon za tekstualni izveštaj.**



### Pitanja:

1. [2 boda] Izvršiti kontrolu kvaliteta FASTQ fajlova alatom FastQC. Priložiti izvrštaj i diskutovati rezultate (da li je neki od kriterijuma koje analizira FastQC označen kao problematičan, i šta taj kriterijum znači?)
 
2. [3 boda] Mapirati sekvencirane readove na referentni genom hg38 upotrebom alata BWA Mem. Upotrebom python biblioteke pysam odrediti sledeće:  
 2a. Koliko je readova uspešno mapirano?  
 2b. Koliko je parova readova mapirano tako da su oba para mapirana?  
 2c. Nacrtati histogram dužina sekvenciranih fragmenata (*template_length*).   
   
3. [4 boda] Izvršiti obradu dobijenog BAM fajla prema GATK protokolu (Markiranje Duplikata, rekalibracija kvaliteta baza)
 3a. Koliki su procenati PCR i optičkih duplikata?

4. [4 bodova] Identifikovati mutacije upotrebom alata Haplotype Caller i filtirtati mutacije predefinisanim filterima (hard filtering) prema Broad preporukama (kao što je rađeno na vežbama).
 4a. Koliko je ukupno mutacija identifikovano, koliko od njih su SNP-ovi, a koliko INDEL-i?
 4b. Koliko mutacija prolazi, a koliko ne prolazi kriterijume filtriranja.
 4c. Izračunati Ti/Tv odnos pre i posle filtriranja.

5. [2 bodova] Anotirati mutacije alatom Funcotator
 5a. Izbrojati različite vrednosti ClinVar značajnosti (anotacija *ClinVar_VCF_CLNSIG*, koliko mutacija je označeno kao *Benign*, *Likely_benign*, itd.)-.

5. [5 bodova] Svi uzorici sadrže određenu količinu kontaminacije DNK materijalom bakterijskog ili virusnog porekla. Većina ovakvih readova se neće mapirati na ljudski genom. Izvući readove koji nisu mapirani u procesu mapiranja, asemblovati ih alatom abyss, i identifikovati organizam od kojeg potiče najduži skafold upotrebom alata Blast.
"""

!apt-get install samtools

!pip install intervaltree

!pip install pysam

!wget https://github.com/broadinstitute/picard/releases/download/2.21.6/picard.jar

!wget -O gatk-4.1.4.1.zip "https://github.com/broadinstitute/gatk/releases/download/4.1.4.1/gatk-4.1.4.1.zip"
!unzip gatk-4.1.4.1.zip
!R -e 'install.packages(c("gplots", "gsalib"))'

!gdown --id 13ESrnOy32eWbPO2jEEMTtLj2vn7NBseS
!gdown --id 1_rvfN87uprNVbIX09ZcdkhLPNjoohgrQ

!git clone https://github.com/lh3/bwa.git
!cd bwa && make

!gzip -d '/content/drive/MyDrive/sample_25.chrom11.exome.pe1.fq.gz'
!gzip -d '/content/drive/MyDrive/sample_25.chrom11.exome.pe2.fq.gz'

"""### 1. Izvršiti kontrolu kvaliteta FASTQ fajlova alatom FastQC. Priložiti izvrštaj i diskutovati rezultate (da li je neki od kriterijuma koje analizira FastQC označen kao problematičan, i šta taj kriterijum znači?)

....(detaljno u izveštaju)

### 2. Mapirati sekvencirane readove na referentni genom hg38 upotrebom alata BWA Mem. Upotrebom python biblioteke pysam odrediti sledeće:
2a. Koliko je readova uspešno mapirano?

2b. Koliko je parova readova mapirano tako da su oba para mapirana?
"""

!pip install bwa

!gsutil ls gs://genomics-public-data

!gsutil ls gs://genomics-public-data/resources/broad/hg38/v0

!gsutil cp gs://genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.fasta .

!gsutil cp gs://genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.fasta.fai .

!bwa/bwa index Homo_sapiens_assembly38.fasta

!gsutil cp gs://genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf . 
!gsutil cp gs://genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf.idx .
!gsutil cp gs://genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.fasta .
!gsutil cp gs://genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.fasta.fai .
!gsutil cp gs://genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.dict .

# !gdown --id 1-0U11U1Z3Dp8vLHoZOtagQl25dFdza-C

!gsutil ls gs://genomics-public-data/resources/broad/hg38/v0



pe1 = '/content/drive/MyDrive/sample_25.chrom11.exome.pe1.fq'
pe2 = '/content/drive/MyDrive/sample_25.chrom11.exome.pe2.fq'

# !bwa/bwa mem -M Homo_sapiens_assembly38.fasta {pe1} {pe2} > aln-pe.sam
# !bwa/bwa mem -M -R '@RG\tID:1\tPL:Illumina\tSM:HG00096' -o HG00096.chr11.exome.sam Homo_sapiens_assembly38.fasta {pe1} {pe2} 
!./bwa/bwa mem -M -R '@RG\tID:1\tPL:Illumina\tSM:HG00096' -o HG00096.chr11.exome.sam Homo_sapiens_assembly38.fasta {pe1} {pe2}

!samtools view -b -o HG00096.chr11.exome.bam HG00096.chr11.exome.sam

!samtools sort -o HG00096.chr11.exome.sorted.bam HG00096.chr11.exome.bam
!samtools index HG00096.chr11.exome.sorted.bam

import pysam

samfile = pysam.AlignmentFile('HG00096.chr11.exome.sorted.bam', 'rb')

cnt = 0
successful = 0
unsuccessful = 0
both_mapped = 0
template_lengths = []
for read in samfile.fetch():
    cnt+=1
    if read.is_unmapped:
        unsuccessful += 1
    else:
        if not read.mate_is_unmapped:
            both_mapped += 1
        successful += 1
    template_lengths.append(read.template_length)

print(f'Mapirano readova: {successful}\nMapiranih parova readova: {both_mapped}\nNemapirano redova:{unsuccessful}')

"""2c. Nacrtati histogram dužina sekvenciranih fragmenata (template_length)."""

import matplotlib.pyplot as plt

plt.hist(template_lengths, bins=201, log=True) 
plt.title('Template lengths')

"""### 3. Izvršiti obradu dobijenog BAM fajla prema GATK protokolu (Markiranje Duplikata, rekalibracija kvaliteta baza) 
3a. Koliki su procenati PCR i optičkih duplikata?
"""

# pe1 = '/content/drive/MyDrive/sample_25.chrom11.exome.pe1.fq'
# pe2 = '/content/drive/MyDrive/sample_25.chrom11.exome.pe2.fq'
# ref = 'Homo_sapiens_assembly38.fasta'
 
# !./bwa/bwa mem -M -R '@RG\tID:1\tPL:Illumina\tSM:HG00096' -o HG00096.chr11.exome.sam {ref} {pe1} {pe2} 
# !samtools view -b HG00096.chr11.exome.sam > HG00096.chr11.exome.bam
# !samtools sort HG00096.chr11.exome.bam > HG00096.chr11.exome.sorted.bam

ibam = 'HG00096.chr11.exome.sorted.bam'
obam = 'HG00096.chr11.exome.deduped.bam'

!java -jar picard.jar MarkDuplicates I={ibam} O={obam} M=dup_metrics.txt

!grep -A2 '## METRICS CLASS' dup_metrics.txt | grep -v '## METRICS CLASS' > report.tsv

import pandas as pd
pd.read_csv('report.tsv', sep='\t')

reader = pysam.AlignmentFile(obam)

dups = [read for read in reader if read.is_duplicate]
print(len(dups))

ibam = 'HG00096.chr11.exome.deduped.bam'
obam = 'HG00096.chr11.exome.recalibrated.bam'
recal = 'HG00096.chr11.exome.recal.table'

dbsnp = 'Homo_sapiens_assembly38.dbsnp138.vcf'
ref = 'Homo_sapiens_assembly38.fasta'

gatk = 'java -jar gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar'

!{gatk} BaseRecalibrator -I {ibam} --known-sites {dbsnp} -O {recal} --reference {ref}

!{gatk} ApplyBQSR -I {ibam} -bqsr {recal} -O {obam}

post_recal = 'HG00096.chr11.exome.post_recal.table'
!{gatk} BaseRecalibrator -I {obam} --known-sites {dbsnp} -O {post_recal} --reference {ref}

!{gatk} AnalyzeCovariates -before {recal} -after {post_recal} -plots 'compare.pdf'

"""### 4. Identifikovati mutacije upotrebom alata Haplotype Caller i filtirtati mutacije predefinisanim filterima (hard filtering) prema Broad preporukama (kao što je rađeno na vežbama). 4a. Koliko je ukupno mutacija identifikovano, koliko od njih su SNP-ovi, a koliko INDEL-i? 4b. Koliko mutacija prolazi, a koliko ne prolazi kriterijume filtriranja. 4c. Izračunati Ti/Tv odnos pre i posle filtriranja.


"""

gatk = 'java -jar gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar'
dbsnp = 'Homo_sapiens_assembly38.dbsnp138.vcf'
ref = 'Homo_sapiens_assembly38.fasta'

ibam = 'HG00096.chr11.exome.recalibrated.bam'
ovcf = 'HG00096.chr11.exome.vcf'

!{gatk} HaplotypeCaller --input {ibam} --output {ovcf} --reference {ref} --dbsnp {dbsnp} -L chr11

def is_snp(variant):
  return len(variant.ref) == 1 and len(variant.alts[0]) == 1

def is_transitions(variant):
  allels = set((variant.ref, variant.alts[0]))
  return allels == {'A', 'G'} or allels == {'C', 'T'}

from collections import Counter

Counter(v.id == None for v in pysam.VariantFile(ovcf))

ti = sum(1 for v in pysam.VariantFile(ovcf) \
         if is_snp(v)\
         and is_transitions(v))

tv = sum(1 for v in pysam.VariantFile(ovcf) \
          if is_snp(v) \
          and not is_transitions(v))

print('Before filter:')
print('Ti:', ti)
print('Tv:', tv)
print('Ti/Tv', ti/tv)

gatk = 'java -jar gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar'

snp_f = "QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0"
indel_f = "QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0" 

ref = 'Homo_sapiens_assembly38.fasta'

ivcf = 'HG00096.chr11.exome.vcf'
isvcf = 'HG00096.chr11.exome.snp.vcf'
iivcf = 'HG00096.chr11.exome.indel.vcf'


osvcf = 'HG00096.chr11.exome.snp.filtered.vcf'
oivcf = 'HG00096.chr11.exome.indel.filtered.vcf'
ovcf = 'HG00096.chr11.exome.filtered.vcf'

!{gatk} SelectVariants -R {ref} -V {ivcf} -O {isvcf} --select-type-to-include SNP
!{gatk} VariantFiltration -R {ref} -V {isvcf} -O {osvcf} -filter "{snp_f}" --filter-name "snp"

!{gatk} SelectVariants -R {ref} -V {ivcf} -O {iivcf} --select-type-to-include INDEL
!{gatk} VariantFiltration -R {ref} -V {iivcf} -O {oivcf} -filter "{indel_f}" --filter-name "indel"

!{gatk} MergeVcfs -I {osvcf} -I {oivcf} -O {ovcf}

def is_filtered(variant):
  return 'PASS' not in variant.filter

def is_snp(variant):
  return len(variant.ref) == 1 and len(variant.alts[0]) == 1

def is_transitions(variant):
  allels = set((variant.ref, variant.alts[0]))
  return allels == {'A', 'G'} or allels == {'C', 'T'}

ovcf = 'HG00096.chr11.exome.filtered.vcf'

# print('SNPs:',
#       sum(1 for v in pysam.VariantFile(ovcf) if is_filtered(v) and is_snp(v)))

# print('INDELs:',
#       sum(1 for v in pysam.VariantFile(ovcf) if is_filtered(v) and not is_snp(v)))

snp = 0
ind = 0

for v in pysam.VariantFile(ovcf):
    if is_snp(v):
        snp += 1
    else:
        ind += 1

print(f'SNPs: {snp}, INDELs: {ind}, Sum: {snp + ind}')

proslo = 0
nije_proslo = 0

for v in pysam.VariantFile(ovcf):
    if is_filtered(v):
        nije_proslo += 1
    else:
        proslo += 1

print(f'Passed filter: {proslo}, Did not pass filter: {nije_proslo}')

ti = sum(1 for v in pysam.VariantFile(ovcf) \
         if not is_filtered(v) \
         and is_snp(v)\
         and is_transitions(v))

tv = sum(1 for v in pysam.VariantFile(ovcf) \
          if not is_filtered(v) \
          and is_snp(v) \
          and not is_transitions(v))

print('After filter:')
print('Ti:', ti)
print('Tv:', tv)
print('Ti/Tv', ti/tv)

"""###5. Anotirati mutacije alatom Funcotator 5a. Izbrojati različite vrednosti ClinVar značajnosti (anotacija ClinVar_VCF_CLNSIG, koliko mutacija je označeno kao Benign, Likely_benign, itd.)-."""

!{gatk} FuncotatorDataSourceDownloader --germline --extract-after-download

ivcf = 'HG00096.chr11.exome.filtered.vcf'
ovcf = 'HG00096.chr11.exome.annotated.vcf'
func = 'funcotator_dataSources.v1.6.20190124g/'

!{gatk} Funcotator -O {ovcf} --ref-version hg38 -R {ref} -V {ivcf} --output-file-format VCF --data-sources-path {func}

reader = pysam.VariantFile(ovcf)
description = reader.header.info['FUNCOTATION'].description
print(description)
funcotations = description[73:].split('|')

print('\n'.join(funcotations))

cnt = 0
results = dict()

for variant in pysam.VariantFile(ovcf):
    try:
        ann = {x:y for x, y in zip(funcotations, variant.info['FUNCOTATION'][0][1:-1].split('|'))}
    except:
        cnt += 1
        pass

    if ann['ClinVar_VCF_CLNSIG']:
        # print(ann['ClinVar_VCF_CLNSIG'])
        if ann['ClinVar_VCF_CLNSIG'] not in results.keys():
            results[ann['ClinVar_VCF_CLNSIG']] = 0
        else:
            results[str(ann['ClinVar_VCF_CLNSIG'])] += 1


for tp, num in results.items():
    if num == 0:
        continue
    print('{} {}'.format(tp, num))

"""### 6. Svi uzorici sadrže određenu količinu kontaminacije DNK materijalom bakterijskog ili virusnog porekla. Većina ovakvih readova se neće mapirati na ljudski genom. Izvući readove koji nisu mapirani u procesu mapiranja, asemblovati ih alatom abyss, i identifikovati organizam od kojeg potiče najduži skafold upotrebom alata Blast."""

# !pip install abyss

!sudo apt-get install autotools-dev automake
!git clone https://github.com/bcgsc/abyss.git
!cd abyss && ./autogen.sh
!cd abyss && ./configure
!cd abyss && make
!cd abyss && sudo make install
 
!sudo apt-get install abyss

#%%time
!git clone https://github.com/sparsehash/sparsehash.git
!cd sparsehash && ./configure
!cd sparsehash && make
!cd sparsehash && sudo make install

# HG00096.chr11.exome.sorted.bam

file = 'HG00096.chr11.filtered.exome.bam'

sf = pysam.AlignmentFile('HG00096.chr11.exome.sorted.bam', 'rb')
f = pysam.AlignmentFile(file, 'wb', template=sf)

for read in sf.fetch():
    if read.is_unmapped:
        f.write(read)

!samtools split HG00096.chr11.filtered.exome.bam

!samtools fastq -1 reads_1.fq -2 reads_2.fq HG00096.chr11.filtered.exome.bam

# !sed 's|.1 |/1 |g' <reads1.fq >reads2.fq

!abyss-pe name=human1 k=64 in='reads_1.fq reads_2.fq'

from glob import glob

for f in glob('*unitigs.fa'):
  try:
      scaffolds = pysam.FastaFile(f)
  except:
      pass
  longest = sorted(zip(scaffolds.lengths, scaffolds.references), 
                   reverse=True)[0][1]
  un = scaffolds.fetch(longest)
  print(f, len(un), un)