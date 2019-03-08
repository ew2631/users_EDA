# users_EDA

Analysis 

Adoption user identification: To identify which users were adopted, I determined the earliest and latest login dates, then created all possible 7-day windows between those two dates. I grouped the login sessions by user_id and ran all login dates for a user through the list of 7-day windows. I created a new column “Adopted”, so if a user logged in more than 3 times in any 7-day window, they were tagged with “1” for adopted and “0” for non-adopted. 

OLS Regression: To prepare the data for the regression, I made a few adjustments: 
1. I dummied out the creation_source variable and dropped one of the variables to avoid multicollinearity 
2.  I created a new variable called time_delta, which is the difference between a user_creation_time and last_session_creation_time 

First, I ran the regression with only the 5 binary variables for creation_source. The results showed that the following variables were statistically significant at the 5% level: org_invite, personal_projects, sign_up. However, they produced negative coefficients, indicating that the dropped variable (guest_invite) has more correlation to adoption. 
Next, I ran the regression with only the user email related variables (enabled_for_marketing_drip, opted_in_for_mailing_list). The results showed that the opted_in_for_mailing_list result was significant. 
Lastly, I ran the regression with all the variables, The results showed org_invite, personal_projects, sign_up, signup_google_authen were all significant but again had negative coefficients, further confirming that guest_invite is most likely correlated to adoption. The time_delta variable was statistically significant, but its coefficient was 1.2e-0.5, making economically insignificant. 


Data Visualizations: 

Bar graphs: For creation_source, I created bar graphs to compare the creation_source for each type of user. org_invite is the highest for both types, but guest_invite is slightly higher for adopted users whereas personal_projects is higher for non-adopted users. 

Mosaics plots: I created mosaic plots for the two binary variables: enabled_for_marketing_drip, opted_in_for_mailing_list. Based on the visualization, it is clear that an adopted user (1.0 on the x axis) and a user enabled for marketing or opted in for the mailing list (1 on the y axis) represents a small fraction of all users, confirming the conclusion from the OLS regression that these variables are not important factors. 


Conclusion: 
Based on the results of the OLS regression and data visualizations, we find that guest_invite from the creation_source variable is the best indicator for adoption. Given these results, the future recommendation is to focus more efforts on creating and marketing incentives to current users to invite their friends to use Asana platform. 

