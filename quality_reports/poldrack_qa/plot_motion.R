##set workingdirectory 
setwd('/home/raid1/reinelt/github/NECOS/r/')

##loading packages
library(ggplot2)
library(Hmisc)
library(gridExtra)
library(cowplot)
library(car)
library(data.table)

#Mandy`s outlier function
add.outlier <- function(p,labvar = as.character(p$mapping$y)){
    df <- data.frame(y = with(p$data,eval(p$mapping$y)),
                     x = with(p$data,eval(p$mapping$x)))
    
    df.l <- split(df,df$x)
    
    mm <- Reduce(rbind, lapply(df.l,FUN = function(df){
        data.frame(y = df$y[df$y <= (quantile(df$y)[2] - 1.5 * IQR(df$y)) | df$y >= (quantile(df$y)[4] + 1.5 * IQR(df$y))],
                   x = df$x[df$y <= (quantile(df$y)[2] - 1.5 * IQR(df$y)) | df$y >= (quantile(df$y)[4] + 1.5 * IQR(df$y))]
        )})
    )
    
    
    mm$x <- factor(mm$x,levels=sort(as.numeric(as.character(unique(p$data[,as.character(p$mapping$x)])))),
                   labels = levels(p$data[,as.character(p$mapping$x)])
    )
    
    names(mm) <- c(as.character(p$mapping$y),as.character(p$mapping$x))
    mm <- merge(p$data[,c(names(mm),labvar)],mm)
    
    p + geom_text(data=mm,
                  aes_string(label=labvar),
                  vjust = -0.5)
}
############
############
####            set summary file and specify parameter to plot

#read in 
master.frame_resting.state <- read.csv(file="/scr/nil1/reinelt/NeCoS/R_data/master.frame_resting.state_movement.csv")
scans_oi = c(2,3)
master.frame_resting.state <- subset(master.frame_resting.state, subset= is.element( master.frame_resting.state$scan_id, scans_oi))
master.frame_resting.state$scan_id <- factor(master.frame_resting.state$scan_id)

scrubbed_df <- read.csv(file='/scr/nil2/reinelt/NECOS/motiion/scrubbed_vols_summary_long.csv')
scrubbed_df[is.na(scrubbed_df)] <- 0
scrubbed_df$scan_id <- gsub('rest2', '2', scrubbed_df$scan_id)
scrubbed_df$scan_id <- gsub('rest3', '3', scrubbed_df$scan_id)

motion_df_scrubed <-  merge(master.frame_resting.state, scrubbed_df, c("NECOS_ID","scan_id"))
motion_df_scrubed$scan_id <- factor(motion_df_scrubed$scan_id)

motion_df_all <-  merge(master.frame_resting.state, scrubbed_df, c("NECOS_ID","scan_id"), all=T)
motion_df_all$scan_id <- factor(motion_df_all$scan_id)

motion_df_all$scrb_total[is.na(motion_df_all$scrb_total)] <- 0
motion_df_all$scrb_consec[is.na(motion_df_all$scrb_consec)] <- 0


subject_scrub_rest2 <- scrubbed_df$NECOS_ID[scrubbed_df$scan_id == 2 & !is.na(scrubbed_df$scrb_total)]
n_sub_rest2_scrub <- length(subject_scrub_rest2)

subject_scrub_rest3 <- scrubbed_df$NECOS_ID[scrubbed_df$scan_id == 3 & !is.na(scrubbed_df$scrb_total)]
n_sub_rest3_scrub <- length(subject_scrub_rest3)


subject_scrub_rest2 == subject_scrub_rest3

print(subject_scrub_rest3)

test <- length(unique(scrubbed_df$NECOS_ID))

boxplot(scrb_total ~ scan_id * group, data=motion_df, notch=TRUE,
        col=(c("gold","darkgreen")),
        main="mean_FD", xlab="rest and group") 


boxp_all <- ggplot(aes(y = scrb_total, x = scan_id, fill = group), data = motion_df_all) + geom_boxplot()


boxp_scrubed <- ggplot(aes(y = scrb_total, x = scan_id, fill = group), data = motion_df_scrubed) + geom_boxplot()

motion_df_scrubed$
t.test()

#function that takes in vector of data and a coefficient,
#returns boolean vector if a certain point is an outlier or not
check_outlier <- function(v, coef=1.5){
    quantiles <- quantile(v,probs=c(0.25,0.75))
    IQR <- quantiles[2]-quantiles[1]
    res <- v < (quantiles[1]-coef*IQR)|v > (quantiles[2]+coef*IQR)
    return(res)
}

#apply this to our data
motion_df[,outlier:=check_outlier(motion_df$scrb_total),by=NECOS_ID]
dat[,label:=ifelse(outlier,"label","")]

#plot
ggplot(dat,aes(x=group,y=value))+geom_boxplot()+geom_text(aes(label=label),hjust=-0.3)








boxp_stress <- ggplot(aes(y = scrb_total, x = scan_id), data = motion_df[motion_df$group=='stress']) + geom_boxplot()
add.outlier(boxp, "NECOS_ID")


ggplot(motion_df, aes(x= scan_id, y= scrb_total), colour=group)+
        geom_boxplot()+
        #scale_y_continuous(limits = c(0, max(stress_df$Serum_Copeptin, na.rm=T)+max(summary_copep_imputed$sd, na.rm=T)))+
        #geom_text(aes(label=ifelse(fbox>2*stress_summ$sd, NECOS_ID,""), hjust=1.1))+
        labs(title="mean FD stress group ")+
        stat_summary(fun.y=mean, colour="darkred", geom="point", 
                 shape=18, size=3,show.legend = FALSE)#+
#scale_y_continuous(limits=c(0, 0.4))


