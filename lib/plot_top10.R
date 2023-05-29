# This code is used to extract the data of the top 10 relative abundance genera of each sample and draw a histogram

library(ggplot2)
library(stringr)
library(dplyr)
library(do)
library(showtext)

Args <- commandArgs(trailingOnly=T)

showtext_auto()

path = paste(Args[2],"/",sep="")

relative_otu = read.csv(Args[1],header=T,sep="\t",row.names=1,skip = 1)

# Clean the classification table of genus level
relative_otu$type <- rownames(relative_otu)
relative_otu <- dplyr::filter(relative_otu, grepl('g__', type))
data <- dplyr::filter(relative_otu, !grepl('g__uncultured', type))
n <- str_split_fixed(data$type, "g__",n = 2)
data$genus <- n[, -1]
rownames(data) <- data$genus
data <- subset(data, select = -c(type,genus))

# Draw a histogram of the top 10 relative abundance on the genus level
fig <- function(data,name){
	data['Top10_genus'] <- Replace(data['Top10_genus'],"_", " ")
	tmp = data
	data = rbind(data,tmp)
	data$position <- rep(80,times = 20)
	data$group <- c(rep('case1',times = 10),rep('case2',times = 10))
	data$label <- c(paste(data[1:10,2],'%',collapse = NULL),rep('',times = 10))
	data[,2] = c(75-data[1:10,2],data[1:10,2])
	data$precent <- c(data[1:10,2]/sum(data[1:10,2]),data[11:20,2]/sum(data[11:20,2]))

	agg <- aggregate(precent ~ Top10_genus, data = data[data$group == 'case1',], sum)
	data$Top10_genus <- factor(data$Top10_genus,levels=agg[order(agg$precent, decreasing = T),"Top10_genus"])

	scale_factor = 2
	
	p <- ggplot(data = data,aes(x = Top10_genus,y = data[,2],fill = group,order = group)) +
		geom_col(width = 0.6) + 
		ylim(0,90) +
		scale_x_discrete(labels=function(x) str_wrap(x, width=14),expand = c(0,0)) +
		scale_fill_manual(values = alpha(c("gray75","deepskyblue2"), c(0.2,0.9))) +
		theme_classic() +
		labs(x = '', y = '') + 
		geom_text(
			data = data,
			aes(x = Top10_genus, y = position,label = label),
			size = scale_factor * 6,
			vjust = 0,
			hjust = 0
		) +
		theme_bw() +
		theme(
			panel.grid = element_blank(),
			panel.border = element_blank(),
			legend.position = 'none',
			axis.text.x = element_blank(),
			axis.text.y = element_text(margin = margin(0,0.5,0,0,'cm'), size = scale_factor * 19, lineheight = 0.3),
			axis.ticks.x = element_blank(),
			axis.ticks.y = element_blank(),
			axis.line.y = element_line(color = "gray65",linewidth = 0.5,linetype = "dashed"),
			plot.margin=unit(c(0.5,0.5,0.5,0.5),'cm')
		) +
		coord_flip(clip = "off")

	ggsave(plot = p, file = name,width = 8,height = 8, units = "cm",dpi = 320,scale = 2)         
}

for (i in colnames(data)){
	sample = data[i]
	sample <- arrange(sample,desc(sample[i]))
	sample <- subset(sample,rownames(sample) %in% rownames(sample)[1:10])
	sample <- round(sample * 100,2)
	sample$Top10_genus = rownames(sample)
	sample = sample[,c(2,1)]
	
	rownames(sample) <- 1:nrow(sample)
	name_EH = paste(path,i,'_top10','.png',sep="")
	fig(sample,name_EH)

}

