###1. This code does (User) Chi-squared tests and Spearman correlation analysis for Social Care surveys data with weights.
### The code has been tested for 'WORK_question_data_and_strata.csv' data set, you can find the test data in the Liz email (15 June 2022 at 21:05).
### Only required Questions variables are selected in the analysis, you can find the selected variables in the spreadsheet 'Questions to include in stats analysis.xlsx'
### The response=1 has been filtered, null values has been removed.

### Input data: You can save two datasets('Questions to include in stats analysis.xlsx','WORK_question_data_and_strata.csv') in any folder, then change the work path to where the folder is using the next line code.
setwd("~/Desktop/R code for user key findings")
### Output: you can find final analysis excel spreadsheet in the same folder 

library(openxlsx)
library(dplyr)
library(wCorr)
require(corrr)
library(weights)


data_questions<-read.xlsx('Questions to include in stats analysis.xlsx')
data_initial<-read.csv('WORK_question_data_and_strata.csv',header = TRUE)
data_initial<-data_initial%>%filter(Response==1)

colnames(data_initial)
colnames(data_questions)
##select questions and admin data as requested.

###data_keep is all the selected variables without weights
###weights_variables_data is all the weights
###selected_questions_weights is selected all the selected variables and weights variables.
data_questions_matrix<-as.matrix(data_questions)
dim(data_questions_matrix)<-c(48*2,1)

clean_data_questions<-na.omit(as.data.frame(data_questions_matrix))
clean_data_questions_list<-as.list(clean_data_questions['V1'])

data_keep<-data_initial%>%dplyr::select(all_of(clean_data_questions_list[['V1']]))
weights_variables_data<-data_initial%>%dplyr::select(Q1_Weight:Q22fSub_Weight)

selected_questions_weights<-cbind(data_keep,weights_variables_data)
names(selected_questions_weights)

##data<-data_initial[all_col]
colnames(data_keep)
colnames(weights_variables_data)




#### Nulls in each question variable  and weight variables.


Null_numbers<-NULL

for(i in names(selected_questions_weights)){
  
  
  Null_numbers[i]<-sum(is.na(selected_questions_weights[i]))
  
}
Null_numbers

#### Nulls in each variable excluding weights variables.
Null_numbers<-NULL

for(i in colnames(data_keep)){
  
  
  Null_numbers[i]<-sum(is.na(data_keep[i]))
}

Null_numbers


dim(data_keep)


##discrete_var<-setdiff(names(data_keep),names(weights_variables))


#####full results
Correlation_ChiSquare_all<-Correlation_all<-Correlation_full<-ChiSquare_all<-ChiSquare_full<-list()

for(var in names(data_keep)){
  Correlation_ChiSquare_all[[var]]<-Correlation_all[[var]]<-ChiSquare_all[[var]]<-NULL
  ChiSquare_all[[var]]<-as.data.frame(matrix(nrow=3,ncol =length(data_keep) ))
  colnames(ChiSquare_all[[var]])<-colnames(data_keep)
  
  Correlation_all[[var]]<-as.data.frame(matrix(nrow=1,ncol =length(data_keep) ))
  colnames(Correlation_all[[var]])<-colnames(data_keep)
  weights_name<-paste0('Weight','_',var)
  
  for(i in colnames(data_keep))
  {
    ChiSquare_all[[var]][i]<-wtd.chi.sq(selected_questions_weights[[var]],selected_questions_weights[[i]],weight = selected_questions_weights[[weights_name]])
    if (weights_name %in% names(weights_variables_data))
    {
      spearman_data<-selected_questions_weights%>%dplyr::select(var,i,weights_name)%>%na.omit()
      Correlation_all[[var]][i]<-weightedCorr(y=spearman_data[[var]], x=spearman_data[[i]], method="spearman", weights=spearman_data[[weights_name]])}
    else 
    {
      spearman_data<-selected_questions_weights%>%dplyr::select(var,i)%>%na.omit()
      Correlation_all[[var]][i]<-weightedCorr(y=spearman_data[[var]], x=spearman_data[[i]], method="spearman")}
  }
  ChiSquare_full[[var]]<-t(ChiSquare_all[[var]])
  colnames(ChiSquare_full[[var]])<-c('Chisq', 'df', 'p.value')
  Correlation_full[[var]]<-t(Correlation_all[[var]])
  colnames(Correlation_full[[var]])<-c('Spearman.correlation')
  Correlation_ChiSquare_all[[var]]<-cbind(ChiSquare_full[[var]],Correlation_full[[var]])
}

## sort the results based on absolute value of Spearman.correlations.

Correlation_ChiSquare_all_copy<-Correlation_ChiSquare_all
for(i in 1:length(Correlation_ChiSquare_all)){
  Correlation_ChiSquare_all_copy[[names(Correlation_ChiSquare_all)[i]]]<-Correlation_ChiSquare_all[[i]][order(abs(Correlation_ChiSquare_all[[i]][,4]),decreasing = T),]}



###save to the Excel

library(openxlsx)

write.xlsx(Correlation_ChiSquare_all_copy,"User full version Weighted Correlation and ChiSquare results.xlsx",rowNames=TRUE)

##### show all the significant results in one sheet 2 

b<-as.data.frame(NULL)

for (i in 1:length(Correlation_ChiSquare_all)) {
  #a<-NULL  
  
  a<-as.data.frame(Correlation_ChiSquare_all[[i]][abs(Correlation_ChiSquare_all[[i]][,4])>=0.4,])%>%na.omit()
  #a<-na.omit(a)
  a<-subset(a,a$Spearman.correlation!=1)
  if (nrow(a)!=0&ncol(a)!=0) 
  {a<-cbind(Varible2=rownames(a),a)
  
  
  rownames(a)<-1:nrow(a)
  Varible1<-names(Correlation_ChiSquare_all)[i]
  library(tibble)
  a<-add_column(a,Varible1, .before='Varible2')
  
  b<-rbind(b,a)}
}


b<-subset(b,b$Varible2!=b$Varible1)
#d<-NULL
d<-b[,c('Varible1','Varible2')]
d<-d[!duplicated(t(apply(d, 1, sort))),]
key_findings_in_one_sheet<-semi_join(b, d)

library(openxlsx)

write.xlsx(key_findings_in_one_sheet,"User significant key findings in one sheet.xlsx")



### 2. As part of the DQ report, we do chi square tests to see if responses differ between particular groups – we don’t apply any weighting to the tests. 

### The data items we look at in the tests are:
### Translated
### Original / Reminder
### Q21 – help to complete the survey
### Q22a – no help to complete the survey
### Q22f – someone completed the survey for me
### Q15a
### Q15b
### Q15c
### Q15d
### Q16a
### Q16b
### Q16c
### Q16d

# We then do Chi-squared tests with the above data items and 5 chosen questions ie questions 1Comb, 2Comb, 7a, 8a and 9a.

chi_square_sample<-read.csv('WORK_question_data_and_strata.csv',header = TRUE)
chi_square_sample2<-chi_square_sample%>%filter(Response==1)%>%select(Translated, OriginalReminder,Q21, Q22a, Q22f, Q15a, Q15b, Q15c, Q15d, Q16a, Q16b,Q16c,Q16d,Q1Comb, Q2Comb, Q7a, Q8a, Q9a)

chisqmatrix <- function(x) {
  names = colnames(x);  num = length(names)
  m = matrix(nrow=num,ncol=num,dimnames=list(names,names))
  for (i in 1:(num-1)) {
    for (j in (i+1):num) {
      m[i,j] = chisq.test(x[,i],x[,j],)$p.value
    }
  }
  return (m)
}
mat2 = chisqmatrix(chi_square_sample2)

ChiSquare_for_reports<-list()
ChiSquare_for_reports$'All items required'<-mat2

library(openxlsx)
Excel_list2<-list()
for (variable in c('All items required')) {
  Excel_list2[[variable]]<-ChiSquare_for_reports[[variable]]
}
write.xlsx(ChiSquare_for_reports,"ChiSquare_for_User_reports.xlsx",rowNames=TRUE)

### 3. percentage of responses for the User report
### output: Please see the percentage of responses in each category for each group in the attachments. 
library(openxlsx)
chi_square_sample<-read.csv('WORK_question_data_and_strata.csv',header = TRUE)
chi_square_sample2<-chi_square_sample%>%filter(Response==1)%>%select(Translated, OriginalReminder,Q21, Q22a, Q22f, Q15a, Q15b, Q15c, Q15d, Q16a, Q16b,Q16c,Q16d,Q1Comb, Q2Comb, Q7a, Q8a, Q9a)

categories_sample3<-chi_square_sample%>%filter(Response==1)%>%select(Q1Comb, Q2Comb, Q7a, Q8a, Q9a)

###pivot percentage
library(janitor)

data_item<-c('Translated', 'OriginalReminder','Q21', 'Q22a', 'Q22f', 'Q15a', 'Q15b', 'Q15c', 'Q15d', 'Q16a', 'Q16b','Q16c','Q16d')
a<-list()
for (j in data_item){
  
 a[[paste0(j,'_percentage')]]<-NULL
  for(i in c('Q1Comb', 'Q2Comb', 'Q7a', 'Q8a', 'Q9a')){
    clean_percentage<-select(chi_square_sample2,i,j)%>%na.omit()
    a[[paste0(j,'_percentage')]][[i]]<-as.data.frame(matrix(nrow=nrow(t(round(prop.table(table(clean_percentage),2)*100,digits=1))),ncol=ncol(t(round(prop.table(table(clean_percentage),2)*100,digits=1)))))
    a[[paste0(j,'_percentage')]][[i]]<-t(round(prop.table(table(clean_percentage),2)*100,digits=1))}
}

for (j in data_item){
write.xlsx(a[[paste0(j,'_percentage')]],paste0(j,'_percentage_User.xlsx'),rowNames=TRUE)
}

