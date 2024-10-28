# download and convert the Collaborative Cross data
#
# supplemental data for Srivastava et al. (2017) Genomes of the Mouse
# Collaborative Cross. Genetics 206:537-556, doi:10.1534/genetics.116.198838
#
# available at Zenodo, doi:10.5281/zenodo.377036

# required libraries
library(data.table)
library(qtl2)
library(qtl2convert)
library(broman)
library(readxl)
set.seed(83763628)


# create RawData/ if not available
rawdata_dir <- "../RawData"
if(!dir.exists(rawdata_dir)) {
  dir.create(rawdata_dir)
}



# download Prob36.zip if not available
zenodo_url <- "https://zenodo.org/record/377036/files/"
zenodo_postpend <- "?download=1"
prob_file <- "Prob36.zip"
distant_file <- paste0(zenodo_url, prob_file, zenodo_postpend)
local_file <- file.path(rawdata_dir, prob_file)
if(!file.exists(local_file)) {
  message("Downloading Prob36.zip")
  download.file(distant_file, local_file)
}

# create directory for data if it doesn't exist
prob_dir <- file.path(rawdata_dir, "Prob36")
if(!dir.exists(prob_dir)) {
  dir.create(prob_dir)
}

# unzip if it hasn't been unzipped
gzfile <- file.path(prob_dir, "CC001-Uncb38V01.csv.gz")
csvfile <- file.path(prob_dir, "CC001-Uncb38V01.csv")
if(!file.exists(gzfile) && !file.exists(csvfile)) {
  message("unzipping Prob36.zip")
  unzip(local_file, exdir=prob_dir)
}

# gunzip all of the Prob36 files
if(!file.exists(csvfile)) {
  files <- list.files(prob_dir, pattern=".csv.gz$")
  
  message("unzipping the probability files")
  
  for(file in files) {
    system(paste("gunzip", file.path(prob_dir, file)))
  }
}
# %%
# load the Prob36 files and determine X, Y, and M genotypes
message("reading the probability files")
files <- list.files(prob_dir, pattern=".csv$")
strains <- sub("\\.csv$", "", files)
probs <- setNames(vector("list", length(strains)), strains)
for(i in seq_along(files)) {
  probs[[i]] <- data.table::fread(file.path(prob_dir, files[i]), data.table=FALSE)
}

##############################
# guess the rest of the cross order
##############################
message("inferring cross order")
mprob <- t(sapply(probs, function(a) colMeans(a[a[,2]=="M", paste0(LETTERS, LETTERS)[1:8]])))
yprob <- t(sapply(probs, function(a) colMeans(a[a[,2]=="Y", paste0(LETTERS, LETTERS)[1:8]])))
xprob <- t(sapply(probs, function(a) colMeans(a[a[,2]=="X", paste0(LETTERS, LETTERS)[1:8]])))
# a bunch where we can't tell Y or M

# also need the supplementary data file
supp_file <- "SupplementalData.zip"
distant_file <- paste0(zenodo_url, supp_file, zenodo_postpend)
local_file <- file.path(rawdata_dir, supp_file)
if(!file.exists(local_file)) {
  message("downloading SupplementalData.zip")
  download.file(distant_file, local_file)
}

# extract just the CCStrains.csv file
csv_file <- "SupplmentalData/CCStrains.csv"
if(!file.exists(csv_file)) {
  message("unzipping SupplementalData.zip")
  unzip(local_file, csv_file, exdir=rawdata_dir)
}
