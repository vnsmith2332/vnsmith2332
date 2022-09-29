import pandas as pd
import requests
import json

class GetCovidData():
    def __init__ (self, country):
        self.country = country
        self.covid_df = pd.DataFrame()
        
        url = "https://covid-api.mmediagroup.fr/v1/history?country="+country+"&status=confirmed" #url to get data
        covid_json_request = requests.get(url) #get data
        covid_dict = json.loads(covid_json_request.text) #put data in dict
        key1 = "All"
        key2 = "dates"
        
        dates = []
        confirmed_cases = []
        for date in covid_dict[key1][key2]: #get data from dict, append data to lists
            if date < '2022-01-01':
                dates.append(date)
                confirmed_cases.append(covid_dict[key1][key2][date])
        
        dates.reverse() #put data in chronological order
        confirmed_cases.reverse()
        
        self.covid_df["Date"] = dates #add dates and cases to df
        self.covid_df["Total Cases"] = confirmed_cases
        self.covid_df[['Year', 'Month', 'Day']] = self.covid_df['Date'].str.split('-', expand = True) #create new columns for date parts
        
        new_cases = [self.covid_df.iloc[i + 1, 1] - self.covid_df.iloc[i, 1] for i in range(len(self.covid_df) - 1)] #math for new cases
        new_cases.insert(0, 0) #starting day = 0 new cases
        self.covid_df["New Cases"] = new_cases #add new cases to df
            
class CovidAnalysis(GetCovidData):
    def __init__(self, country):
        GetCovidData.__init__ (self, country)
        self.country = country
        self.avg_new_cases = self.covid_df.iloc[len(self.covid_df) - 1, 1]/len(self.covid_df)
        
        max_new_cases_index = self.covid_df.index[self.covid_df['New Cases'] == max(self.covid_df["New Cases"])] #store index for max new cases
        self.high_date = self.covid_df.iloc[max_new_cases_index[0], 0] #access date of max new cases using index
        
        zero_new_cases_indices = []    
        for index, row in self.covid_df.iterrows(): #find all indices w/ 0 new cases
            if row['New Cases'] == 0:
                zero_new_cases_indices.append(index)
            else:
                pass
        
        self.no_cases_date = self.covid_df.iloc[max(zero_new_cases_indices), 0] #high index = last day w/ 0 new cases
        
        grouped_covid_df = self.covid_df.groupby(['Year', 'Month']).sum() #group df
        highest_month_index = grouped_covid_df.index[grouped_covid_df['New Cases'] == max(grouped_covid_df["New Cases"])] #indexes for max/min
        lowest_month_index = grouped_covid_df.index[grouped_covid_df['New Cases'] == min(grouped_covid_df["New Cases"])]
        
        self.high_month = highest_month_index[0][0]+"-"+highest_month_index[0][1] #access MultiIndices
        self.low_month = lowest_month_index[0][0]+"-"+lowest_month_index[0][1]
                
    def get_country(self):
        return self.country
    
    def get_avg_new_cases(self):
        return self.avg_new_cases
        
    def get_high_date(self):
        return self.high_date
        
    def get_no_cases_date(self):
        return self.no_cases_date
        
    def get_high_month(self):
        return self.high_month
        
    def get_low_month(self):
        return self.low_month
        
def main():
    countries = ["US", "Russia", "Germany"]
    for country in countries:
        results = CovidAnalysis(country)
        print("Country:", results.get_country())
        print("Avg New Cases:", results.get_avg_new_cases())
        print("Date with Most New Cases:", results.get_high_date())
        print("Most Recent Date with no New Cases:", results.get_no_cases_date())
        print("Month with Most New Cases:", results.get_high_month())
        print("Month with Fewest New Cases:", results.get_low_month())
        print("--------------\n")
        
if __name__ == "__main__":
    main()
                    
                            
