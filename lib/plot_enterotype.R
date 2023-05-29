# This code is using for enterotype analysis

library(dplyr)
library(stringr)
library(cluster)
library(clusterSim)
library(ade4)
library(ggplot2)
library(wesanderson)

Args <- commandArgs(trailingOnly=T)

relative_otu <- read.csv(Args[1], header = T, sep = "\t", row.names = 1, skip = 1)

relative_otu$type <- rownames(relative_otu)
relative_otu <- dplyr::filter(relative_otu, grepl('g__', type))
data <- dplyr::filter(relative_otu, !grepl('g__uncultured', type))
n <- str_split_fixed(data$type, "g__", 2)
data$genus <- n[, -1]
rownames(data) <- data$genus
data <- subset(data, select = -c(type,genus))

# Calculate the JSD distance between samples based on the abundance of relative abundance
dist.JSD <- function(inMatrix, pseudocount = 0.000001, ...) {
  KLD <- function(x,y) sum(x *log(x/y))
  JSD<- function(x,y) sqrt(0.5 * KLD(x, (x+y)/2) + 0.5 * KLD(y, (x+y)/2))
  matrixColSize <- length(colnames(inMatrix))
  colnames <- colnames(inMatrix)
  resultsMatrix <- matrix(0, matrixColSize, matrixColSize)
  
  inMatrix <- apply(inMatrix, 1:2, function(x) ifelse (x==0, pseudocount, x))
  
  for(i in 1:matrixColSize) {
    for(j in 1:matrixColSize) { 
      resultsMatrix[i,j] <- JSD(as.vector(inMatrix[, i]), as.vector(inMatrix[,j]))
    }
  }
  colnames -> colnames(resultsMatrix) -> rownames(resultsMatrix)
  as.dist(resultsMatrix) -> resultsMatrix
  attr(resultsMatrix, "method") <- "dist"
  return(resultsMatrix) 
}

# PAM clustering based on JSD distance
pam.clustering <- function(x, k) {
  require(cluster)
  cluster <- as.vector(pam(as.dist(x), k, diss=TRUE)$clustering)
  return(cluster)
}

data.dist <- dist.JSD(data)
                   
require(clusterSim)
nclusters <- NULL

# Calculate each CH value for cluster type from 1 to 20
for (k in 1:20) { 
  if (k == 1) {
    nclusters[k] <- NA
  } else {
    data.cluster_temp <- pam.clustering(data.dist, k)
    nclusters[k] <- index.G1(t(data), data.cluster_temp, d = data.dist,
                             centrotypes = "medoids")
  }
}

nclusters[1] <- 0
k <- which.max(nclusters)
data.cluster <- pam.clustering(data.dist, k = k)
obs.pcoa <- dudi.pco(data.dist, scannf = F, nf = k)

# Draw a PCoA figure of cluster
label <- paste(c("cluster"), c(1:k))
color <- wes_palette("Zissou1", k, type = 'discrete')

pcoa1_eig<-obs.pcoa$eig[1:2]/sum(obs.pcoa$eig) 
sample_site1<-data.frame({obs.pcoa$li})[1:2] 
sample_site1$names <- rownames(sample_site1) 
names(sample_site1)[1:2] <- c("PCo1","PCo2")
p <- ggplot(sample_site1, mapping=aes(PCo1, PCo2,color=as.factor(data.cluster),fill = as.factor(data.cluster))) + 
  geom_point(aes(fill = as.factor(data.cluster)),size = 4.5,shape = 20) +
  scale_color_manual(values = color,labels = label) +
  stat_ellipse(level = 0.65,geom = "polygon",alpha = 1/4,linetype = 1,linewidth = 0.5,show.legend = FALSE) + 
  scale_fill_manual(values = color,labels = label) +
  theme_bw() +
  theme(
       legend.title = element_blank(),
       legend.position = c(0.5,1.05),
       legend.direction = "horizontal",
       panel.grid = element_line(color = "grey80",linewidth = 0.55,linetype=2),
       panel.grid.major = element_line(color = "grey80",linewidth = 0.55,linetype=2),
       panel.grid.minor = element_line(color = "grey80",linewidth = 0.55,linetype=2),
       panel.border = element_rect(color = "grey80",linewidth = 1),
       plot.margin = unit(c(1,1,1,1),'cm')
  ) +
  geom_point()

output <- paste(Args[2], "/", "Enterotype.png", sep="")
ggsave(plot = p, file = output,width = 16,height = 16, units = "cm",dpi = 320)

# Draw a boxplot of designated genus relative abundance
if (Args[3] != 0){

  need_list <- strsplit(Args[3],",")
  for (need in need_list[[1]]){
    data_class <- t(data[c(need), ])
    data_class <- as.data.frame(data_class)
    data_class$group <- data.cluster
    colnames(data_class)[colnames(data_class) == need] <- 'value'
    data_class$group <- factor(data_class$group)
    scale_color <- rep("gray", k)

    pb <- ggplot(data_class,aes(x = group,y = value,fill = group))+
      stat_boxplot(geom = "errorbar",width = 0.2,aes(color = "black"))+
      geom_boxplot(size = 0.3,fill = "white",outlier.fill = "white",outlier.color = "white")+
      geom_jitter(aes(fill = group),width = 0.2,shape = 21,size = 3)+
      scale_color_manual(values = "black")+
      scale_fill_manual(values = scale_color) +
      theme_bw()+
      theme(legend.position="none",
            axis.text.x = element_text(colour = "black", size = 12),
            axis.text.y = element_text(colour = "black", size = 12),
            axis.title.y = element_text(colour = "black", size = 14),
            axis.title.x = element_text(colour = "black", size = 14),
            panel.grid.major = element_blank(),
            panel.grid.minor = element_blank())+
       ylab(need)

    output_pb <- paste(Args[2], "/", need, "_comparion.png", sep = "")
    ggsave(plot = pb, file = output_pb, width = 16,height = 16, units = "cm", dpi = 320)
  }
}

