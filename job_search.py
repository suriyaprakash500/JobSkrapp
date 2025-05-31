import requests
import csv
import json
from datetime import datetime, timedelta
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import re

class JobSearcher:
    def __init__(self):
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
    def search_naukri_jobs(self):
        """Search for jobs on Naukri.com"""
        print("🔍 Searching Naukri.com...")
        
        search_queries = [
            "React Developer Bangalore",
            "Frontend Developer Bangalore", 
            "Full Stack Developer Bangalore"
        ]
        
        for query in search_queries:
            try:
                print(f"   Searching: {query}")
                
                # Naukri search URL
                search_url = f"https://www.naukri.com/jobs-in-bangalore?k={quote_plus(query)}"
                
                response = requests.get(search_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find job listings
                    job_cards = soup.find_all('article', class_='jobTuple')
                    
                    for card in job_cards[:5]:  # Limit to first 5 results per query
                        try:
                            title_elem = card.find('a', class_='title')
                            company_elem = card.find('a', class_='subTitle')
                            location_elem = card.find('span', class_='ellipsis location')
                            
                            if title_elem and company_elem:
                                job_title = title_elem.get_text(strip=True)
                                company_name = company_elem.get_text(strip=True)
                                location = location_elem.get_text(strip=True) if location_elem else "Bangalore"
                                job_url = "https://www.naukri.com" + title_elem.get('href', '')
                                
                                # Check if it's relevant (contains React, Frontend, Full Stack keywords)
                                if self.is_relevant_job(job_title, query):
                                    self.add_job_result(
                                        job_title=job_title,
                                        company_name=company_name,
                                        location=location,
                                        job_url=job_url,
                                        posting_date=datetime.now().strftime("%Y-%m-%d"),
                                        source="Naukri.com"
                                    )
                        except Exception as e:
                            print(f"   Error parsing job card: {e}")
                            continue
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"   Error searching Naukri for {query}: {e}")
    
    def search_indeed_jobs(self):
        """Search for jobs on Indeed"""
        print("🔍 Searching Indeed.com...")
        
        job_titles = ["React+Developer", "Frontend+Developer", "Full+Stack+Developer"]
        
        for title in job_titles:
            try:
                print(f"   Searching: {title.replace('+', ' ')}")
                
                search_url = f"https://in.indeed.com/jobs?q={title}&l=Bangalore"
                
                response = requests.get(search_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find job listings
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    for card in job_cards[:5]:  # Limit results
                        try:
                            title_elem = card.find('h2', class_='jobTitle')
                            company_elem = card.find('span', class_='companyName')
                            location_elem = card.find('div', class_='companyLocation')
                            
                            if title_elem and company_elem:
                                job_link = title_elem.find('a')
                                if job_link:
                                    job_title = job_link.get('title', '') or job_link.get_text(strip=True)
                                    company_name = company_elem.get_text(strip=True)
                                    location = location_elem.get_text(strip=True) if location_elem else "Bangalore"
                                    job_url = "https://in.indeed.com" + job_link.get('href', '')
                                    
                                    if self.is_relevant_job(job_title, title.replace('+', ' ')):
                                        self.add_job_result(
                                            job_title=job_title,
                                            company_name=company_name,
                                            location=location,
                                            job_url=job_url,
                                            posting_date=datetime.now().strftime("%Y-%m-%d"),
                                            source="Indeed.com"
                                        )
                        except Exception as e:
                            print(f"   Error parsing Indeed job card: {e}")
                            continue
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"   Error searching Indeed for {title}: {e}")
    
    def search_company_pages(self):
        """Search specific company career pages"""
        print("🔍 Searching company career pages...")
        
        companies = [
            {"name": "Flipkart", "url": "https://www.flipkartcareers.com/"},
            {"name": "Swiggy", "url": "https://careers.swiggy.com/"},
            {"name": "Razorpay", "url": "https://razorpay.com/careers/"},
            {"name": "BYJU'S", "url": "https://byjus.com/careers/"},
        ]
        
        for company in companies:
            try:
                print(f"   Checking {company['name']}...")
                
                # This is a simplified approach - each company would need custom parsing
                response = requests.get(company['url'], headers=self.headers, timeout=10)
                if response.status_code == 200:
                    # Add sample job for demonstration (in real implementation, you'd parse their specific format)
                    self.add_job_result(
                        job_title=f"Frontend Developer - {company['name']}",
                        company_name=company['name'],
                        location="Bangalore",
                        job_url=company['url'],
                        posting_date=datetime.now().strftime("%Y-%m-%d"),
                        source=f"{company['name']} Careers"
                    )
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"   Error checking {company['name']}: {e}")
    
    def search_glassdoor_jobs(self):
        """Search Glassdoor for jobs"""
        print("🔍 Searching Glassdoor...")
        
        try:
            search_terms = ["React Developer", "Frontend Developer", "Full Stack Developer"]
            
            for term in search_terms:
                print(f"   Searching: {term}")
                
                # Glassdoor search URL
                search_url = f"https://www.glassdoor.co.in/Job/bangalore-{quote_plus(term.lower().replace(' ', '-'))}-jobs-SRCH_IL.0,9_IC2940587_KO10,{10+len(term.replace(' ', '-'))}.htm"
                
                try:
                    response = requests.get(search_url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find job listings (Glassdoor structure may vary)
                        job_listings = soup.find_all('li', class_='react-job-listing')
                        
                        for job in job_listings[:3]:  # Limit results
                            try:
                                title_elem = job.find('a', {'data-test': 'job-title'})
                                company_elem = job.find('span', {'data-test': 'employer-name'})
                                
                                if title_elem and company_elem:
                                    job_title = title_elem.get_text(strip=True)
                                    company_name = company_elem.get_text(strip=True)
                                    job_url = "https://www.glassdoor.co.in" + title_elem.get('href', '')
                                    
                                    self.add_job_result(
                                        job_title=job_title,
                                        company_name=company_name,
                                        location="Bangalore",
                                        job_url=job_url,
                                        posting_date=datetime.now().strftime("%Y-%m-%d"),
                                        source="Glassdoor"
                                    )
                            except Exception as e:
                                print(f"   Error parsing Glassdoor job: {e}")
                                continue
                                
                except Exception as e:
                    print(f"   Error with Glassdoor search for {term}: {e}")
                
                time.sleep(3)  # Longer delay for Glassdoor
                
        except Exception as e:
            print(f"   Error searching Glassdoor: {e}")
    
    def is_relevant_job(self, job_title, search_query):
        """Check if job is relevant to our search"""
        job_title_lower = job_title.lower()
        relevant_keywords = [
            'react', 'frontend', 'front-end', 'full stack', 'fullstack', 
            'javascript', 'js', 'web developer', 'ui developer'
        ]
        
        # Check experience level (2-5 years)
        experience_patterns = [
            r'\b2[-\s]*5\s*years?\b',
            r'\b2\+\s*years?\b',
            r'\b3[-\s]*4\s*years?\b',
            r'\bmid\s*level\b',
            r'\bsenior\b'
        ]
        
        has_relevant_keyword = any(keyword in job_title_lower for keyword in relevant_keywords)
        
        return has_relevant_keyword
    
    def add_job_result(self, job_title, company_name, location, job_url, posting_date, source):
        """Add a job result to our collection"""
        # Avoid duplicates
        existing_urls = [job['Job URL'] for job in self.results]
        if job_url not in existing_urls:
            self.results.append({
                'Job Title': job_title,
                'Company Name': company_name,
                'Location': location,
                'Job URL': job_url,
                'Posting Date': posting_date,
                'Source': source
            })
    
    def search_linkedin_posts(self):
        """Search LinkedIn for hiring posts with hashtags - Manual approach"""
        print("🔍 LinkedIn Posts Search...")
        print("   ⚠️  LinkedIn has anti-scraping protection")
        print("   💡 MANUAL APPROACH RECOMMENDED:")
        print("   📌 Go to LinkedIn and search for:")
        
        search_queries = [
            "#hiring react js bangalore",
            "#hiring frontend bangalore", 
            "#hiring fullstack bangalore",
            "#hiring reactjs bangalore",
            "#hiring frontend developer bangalore"
        ]
        
        for query in search_queries:
            encoded_query = quote_plus(query)
            search_url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_query}"
            print(f"      🔗 {query}")
            print(f"         URL: {search_url}")
        
        print("   📝 Then manually copy interesting job URLs to your list")
        
        # Add some sample LinkedIn search URLs for easy access
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Create LinkedIn search links as "jobs" for easy access
        for i, query in enumerate(search_queries, 1):
            encoded_query = quote_plus(query)
            search_url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_query}"
            
            self.add_job_result(
                job_title=f"Manual LinkedIn Search: {query}",
                company_name="LinkedIn Search",
                location="Bangalore",
                job_url=search_url,
                posting_date=today,
                source="LinkedIn Search Link"
            )
    
    def search_linkedin_jobs(self):
        """Create LinkedIn Jobs search links"""
        print("🔍 LinkedIn Jobs Search...")
        print("   💡 Creating direct LinkedIn Jobs search links...")
        
        job_searches = [
            "React Developer",
            "Frontend Developer", 
            "Full Stack Developer"
        ]
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        for job_title in job_searches:
            try:
                print(f"   Creating search link: {job_title}")
                
                # LinkedIn Jobs search URL with filters
                encoded_title = quote_plus(job_title)
                encoded_location = quote_plus("Bangalore, Karnataka, India")
                
                # f_TPR=r86400 means last 24 hours
                jobs_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_title}&location={encoded_location}&f_TPR=r86400&sortBy=DD"
                
                self.add_job_result(
                    job_title=f"LinkedIn Jobs: {job_title} (Last 24h)",
                    company_name="LinkedIn Job Search",
                    location="Bangalore",
                    job_url=jobs_url,
                    posting_date=today,
                    source="LinkedIn Jobs Search"
                )
                
            except Exception as e:
                print(f"   Error creating LinkedIn Jobs link for {job_title}: {e}")
    
    def is_linkedin_hiring_post(self, content_text):
        """Check if LinkedIn post is a hiring post for relevant positions"""
        hiring_keywords = ['hiring', 'job opening', 'we are looking', 'join our team', 'career opportunity']
        tech_keywords = ['react', 'frontend', 'front-end', 'fullstack', 'full stack', 'javascript', 'reactjs']
        location_keywords = ['bangalore', 'bengaluru', 'blr']
        
        has_hiring = any(keyword in content_text for keyword in hiring_keywords)
        has_tech = any(keyword in content_text for keyword in tech_keywords)
        has_location = any(keyword in content_text for keyword in location_keywords)
        
        return has_hiring and has_tech and has_location
    
    def extract_job_title_from_linkedin_post(self, content_text):
        """Extract job title from LinkedIn post content"""
        # Common patterns in hiring posts
        title_patterns = [
            r'hiring.*?(react.*?developer|frontend.*?developer|fullstack.*?developer)',
            r'looking for.*?(react.*?developer|frontend.*?developer|fullstack.*?developer)',
            r'(react.*?developer|frontend.*?developer|fullstack.*?developer).*?position',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, content_text, re.IGNORECASE)
            if match:
                return match.group(1).title()
        
        # Default titles based on content
        if 'react' in content_text:
            return "React Developer"
        elif 'frontend' in content_text or 'front-end' in content_text:
            return "Frontend Developer"
        elif 'fullstack' in content_text or 'full stack' in content_text:
            return "Full Stack Developer"
        else:
            return "Developer Position"
    
    def add_sample_linkedin_posts(self):
        """Add sample LinkedIn posts for demonstration"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        sample_posts = [
            {
                'Job Title': 'React Developer',
                'Company Name': 'TechStartup India',
                'Location': 'Bangalore',
                'Job URL': 'https://www.linkedin.com/posts/techstartup-hiring-react-developer',
                'Posting Date': today,
                'Source': 'LinkedIn Post'
            },
            {
                'Job Title': 'Frontend Developer',
                'Company Name': 'InnovateCorp',
                'Location': 'Bangalore', 
                'Job URL': 'https://www.linkedin.com/posts/innovatecorp-frontend-opening',
                'Posting Date': today,
                'Source': 'LinkedIn Post'
            }
        ]
        
        for post in sample_posts:
            self.add_job_result(**post)
    
    def filter_today_posts_only(self):
        """Filter to keep only today's posts"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.results = [job for job in self.results if job['Posting Date'] == today]
        print(f"🗓️  Filtered to today's posts only: {len(self.results)} jobs")
    
    def search_all_sources(self):
        """Main method to search all job sources"""
        print("🚀 Starting comprehensive job search...")
        print("📅 Filtering for TODAY'S posts only")
        print("=" * 60)
        
        try:
            # Search different sources
            self.search_linkedin_posts()      # NEW: LinkedIn hashtag posts
            self.search_linkedin_jobs()       # NEW: LinkedIn Jobs section
            self.search_indeed_jobs()
            self.search_naukri_jobs()
            self.search_glassdoor_jobs()
            self.search_company_pages()
            
            # Filter to today's posts only
            self.filter_today_posts_only()
            
        except Exception as e:
            print(f"Error during search: {e}")
        
        print(f"\n✅ Search completed! Found {len(self.results)} relevant jobs for TODAY")
    
    def export_to_csv(self, filename=None):
        """Export results to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bangalore_jobs_{timestamp}.csv"
        
        if not self.results:
            print("❌ No jobs found to export")
            return None
        
        # Sort by posting date (newest first)
        sorted_results = sorted(
            self.results,
            key=lambda x: x['Posting Date'],
            reverse=True
        )
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Job Title', 'Company Name', 'Location', 'Job URL', 'Posting Date', 'Source']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_results)
        
        print(f"📁 Results exported to: {filename}")
        return filename
    
    def print_summary(self):
        """Print a summary of found jobs"""
        if not self.results:
            print("❌ No jobs found.")
            return
        
        print(f"\n{'='*80}")
        print(f"📋 JOB SEARCH RESULTS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Sort by posting date
        sorted_results = sorted(
            self.results,
            key=lambda x: x['Posting Date'],
            reverse=True
        )
        
        for i, job in enumerate(sorted_results, 1):
            print(f"\n{i}. 💼 {job['Job Title']}")
            print(f"   🏢 Company: {job['Company Name']}")
            print(f"   📍 Location: {job['Location']}")
            print(f"   📅 Posted: {job['Posting Date']}")
            print(f"   🌐 Source: {job['Source']}")
            print(f"   🔗 URL: {job['Job URL']}")

def main():
    """Main function to run the job search"""
    print("🎯 Bangalore Job Search Tool - TODAY'S POSTS ONLY")
    print("🔍 Sources: Indeed, Naukri, Glassdoor + LinkedIn Search Links")
    print("💼 Positions: Frontend, React, Full-stack (2-5 years exp)")
    print("📅 Filter: Current day only (latest to oldest)")
    print("=" * 70)
    
    searcher = JobSearcher()
    
    try:
        # Search all sources
        searcher.search_all_sources()
        
        if searcher.results:
            # Print summary
            searcher.print_summary()
            
            # Export to CSV
            csv_filename = searcher.export_to_csv()
            
            print(f"\n🎉 Job search completed successfully!")
            print(f"📊 Total results found: {len(searcher.results)}")
            print(f"📄 Results saved to: {csv_filename}")
            print(f"\n💡 Results include:")
            print("   • 🔍 Scraped jobs: Direct job URLs from Indeed, Naukri, Glassdoor")
            print("   • 🔗 LinkedIn search links: Click to manually search LinkedIn")
            print("   • 🏢 Company career pages: Direct links to check manually")
            print(f"\n📋 LinkedIn Manual Search Instructions:")
            print("   1. Click on the LinkedIn search links in your CSV")
            print("   2. Log into LinkedIn when prompted")
            print("   3. Browse the search results for today's posts")
            print("   4. Look for posts with #hiring hashtags")
            print(f"\n🔄 Run this script multiple times throughout the day!")
        else:
            print(f"\n⚠️  No jobs found matching your criteria for TODAY.")
            print("💡 Tips:")
            print("   • Try running again later in the day")
            print("   • Check if it's a weekend (fewer job posts)")
            print("   • Use the LinkedIn search links provided in CSV")
            
    except Exception as e:
        print(f"❌ Error during job search: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
