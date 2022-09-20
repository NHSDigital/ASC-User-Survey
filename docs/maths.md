# Maths

## Stratification

### Why stratify

In the survey, certain groups were oversampled. This means they were sent more surveys than other groups. This might be because they are a marginalised group that it is vital to get statistically significant results for. However, just because a group was oversampled doesn't mean that you want that group to dominate the results.

Imagine one group makes up 10% of a local authority's population in social care, but make up 70% of the respondents to the questionnaire. If you take a naive average of people's response to the questions, you will find the opinions of that group dominate the answer.

Such a group might be all those people with learning difficulties.

We perform a process which works out how people answered a question within each small group. It then adds that group's answer to the total but making it proportional to that groups true population size. So in the example above, the oversampled group's answer would be "shrunk" by division until it took up only 10% of the final answer.

The small groups that people are divided into we call **subgroups**.

Note: In statistics literature, subgroups are normally called strata. However, in adult social care, we divide the entire population into what we call strata. There are only 4 and you can read about them here (https://files.digital.nhs.uk/BD/6D7209/pss-ascs-eng-1819-Methodology_report.pdf page 6). However, when we are doing stratified averages, the small groups that we sum up over are normally groups like "stratum 2 in local authority 211".

The least confusing naming was to have **stratum** or **strata** refer to the 4 strata that we split the population into, and then **subgroup** refer to the small groups that we split people into when we perform this stratified average process.

The large groups that we sum together to are called **supergroups**. A supergroup might be a local authority, or it might be all males in England, or something else.

For example we might have the supergroup "Males" and it would be formed up of subgroups "Males in LA 211 Stratum 3", "Males in LA 311 Stratum 4", etc

### How the maths combines it

Lots of the ASCS transformations involve a process whereby
we know how different subgroups of people answered a question

    E.g:
    Within LA 211 Stratum 1's male   population, 34.5% of people answered "4" to q3a
        (of those in the sample who responded)
    Within LA 211 Stratum 2's male   population, 43.2% of people answered "4" to q3a
        (of those in the sample who responded)
    Within LA 211 Stratum 1's female population, 38.2% of people answered "4" to q3a
        (of those in the sample who responded)

we also know how large each subgroup is, or have an estimate

    E.g:
    LA 211 Stratum 1's male population has 1234 people
    LA 211 Stratum 2's male population has 3456 people
    LA 211 Stratum 1's female population has 2345 people

We often want one statistic to capture how a bigger group (containing multiple subgroups) answer a question.

    How many men answer "4" to q3a?

Or more accurately

    How many men would answer "4" to question 3a, if we had responses from 100% of the population?

The information that we have allows us to answer this via a simple method

    1)  Get the estimated number of people in each LA Stratum who would answer "4" using

        estimated number of men who would answer "4" in the LA stratum
        = population of men in LA stratum * proportion of people in the sample who responded "4"

    2)  Add together the estimates for each LA stratum, to get the total men in the country who would answer that way.

Effectively this function does that. This is the estimatimated population column outputted by the function.

Once we have reached this step we are easily able to answer a second related question.

    What % of men would answer "4" to q3a?
        (if we sampled 100% of the population)

Because if we know that

    345 men would answer "1" to q3a
    278 men would answer "2" to q3a
    1890 men would answer "3" to q3a
    9834 men would answer "4" to q3a

then the percentage that answered the question each way is simply a matter of doing

    estimated % of men that would answer "4" to q3a
    = estimated number of men who would answer "4" to q3a if we got responses from 100% of the population
        / total number of men in 100% of the population

Why couldn't we calculate this % by just counting in the original questionnaire response data
the proportion of men who answered "4" to q3a?
Imagine Ealing council and Brighton council have the same number of men in adult social care
but Ealing only successfully collect survey data from half the number of men that Brighton do.
This would mean that Ealing would form a smaller proportion of the final answer than Brighton
despite having the same share of the true population, if we were using the naieve method.

Our method avoids this.
If 10% of men sampled by Ealing answer "4" to q3a
and the male population in Ealing is 864
then this method will calculate that 86.4 men in Ealing would answer "4" to q3a.
Note how, no matter how many people Ealing council sample, this number would stay the same.
Even if they sample many fewer people than Brighton.
Furthermore, the final population % is calculated from this estimated number of men,
and so the percentage would also not change even if Ealing sample fewer people.

For efficiency, this function creates many of these weighted average statistics simultaneously.

Continuing the example, one function call would also answer
What % of men answered "1", "2", "3", "4", "5" to q3a respectively?
What % of women answered "1", "2", "3", "4", "5" to q3a respectively?
What % of people of other gender answered "1", "2", "3", "4", "5" to q3a respectively?

### How to get the estimated population size?

We need to give an estimated population to every subgroup
Each subgroup has one demographic characteristic (e.g: male) and is in one LA stratum

We want the group to have a weight proportional to its true size in the world
So when combining subgroups into the larger group, the subgroup takes up a propotion of the answer equal to its true size
With the stratums inside the LA we knew the population sizes exactly
We do not know the sizes of the demographic subgroups in each LA stratum.

We estimate the group's size using
weight of dem la stratum = estimated true population of dem la stratum
                            = la stratum population
                            * (number of people in dem la stratum that responded
                                / number of people in la stratum that responded)

Why does this estimate work?
If we assume that all people in an LA stratum are equally likely to respond to the survey
then we can say that if a demographic group (say, men) make up 40% of the la stratum
we are likely to see that 40% of the people who responded were men.

In other words
decent estimate for % of an la stratum that is one demographic group
= observed % of the respondents in the demographic group that are that demo group
= number of people in dem la stratum that responded
    / number of people in la stratum that responded

The final step is just to say
if some demographic group (e.g men) is 40% of this LA stratum
and the LA stratum has a population of 1000
then the number of men is going to be
1000 * 0.4 = 400
