# JobSpy Provider Testing Suite

This directory contains organized test and debug scripts for each job board provider.

## 📁 **Directory Structure**

```
tests/
├── indeed/
│   ├── debug_indeed.py           # Comprehensive Indeed debugging
│   └── test_indeed.py            # Basic Indeed testing
├── ziprecruiter/
│   ├── debug_ziprecruiter.py     # ZipRecruiter debugging
│   ├── test_ziprecruiter.py      # Basic ZipRecruiter testing
│   ├── test_ziprecruiter_residential.py  # iproyal proxy testing
│   └── iproyal_example.py        # iproyal usage example
├── linkedin/
│   ├── debug_linkedin.py         # LinkedIn debugging
│   └── test_linkedin.py          # Basic LinkedIn testing
├── glassdoor/
│   ├── debug_glassdoor.py        # Glassdoor debugging
│   └── test_glassdoor.py         # Basic Glassdoor testing
├── google/
│   ├── debug_google.py           # Google Jobs debugging
│   └── test_google.py            # Basic Google Jobs testing
└── results/                      # Test output files
```

## 🔧 **Debug Scripts**

Each provider has a comprehensive debug script that tests:

### **Indeed** (`tests/indeed/debug_indeed.py`)
- ✅ **Mobile user agents** with iOS TLS fingerprinting
- ✅ **Proxy support** for IP blocking issues
- ✅ **Indeed-specific search syntax** (quotes, OR, exclusions)
- ✅ **Parameter conflict testing** (hours_old vs job_type vs easy_apply)
- ✅ **Header debugging** for 403 errors

**Key Indeed Issues:**
- Only ONE of these parameters can be used: `hours_old`, `job_type & is_remote`, `easy_apply`
- Use proper search syntax: `"software engineer" python OR java -marketing -sales`
- Indeed searches descriptions (causes unrelated results without filtering)

### **ZipRecruiter** (`tests/ziprecruiter/debug_ziprecruiter.py`)
- ✅ **CloudScraper** for Cloudflare bypass
- ✅ **iproyal residential proxy** rotation
- ✅ **Mobile user agent** simulation
- ✅ **Multiple location testing**

### **LinkedIn** (`tests/linkedin/debug_linkedin.py`)
- ✅ **Desktop user agent** strategy
- ✅ **Rate limiting** behavior testing
- ✅ **Full description fetching** (`linkedin_fetch_description=True`)
- ✅ **Proxy support** for large-scale scraping

### **Glassdoor** (`tests/glassdoor/debug_glassdoor.py`)
- ✅ **GraphQL API** with CSRF tokens
- ✅ **Desktop user agent** strategy
- ✅ **Multiple country support**
- ✅ **Remote job filtering**

### **Google Jobs** (`tests/google/debug_google.py`)
- ✅ **Desktop user agent** strategy
- ✅ **Google-specific search terms** (`google_search_term`)
- ✅ **Time-based filtering** ("since yesterday", "posted today")
- ✅ **Natural language search** syntax

## 🚀 **Quick Start**

### **Test Individual Providers**
```bash
# Test Indeed
python tests/indeed/debug_indeed.py

# Test ZipRecruiter with iproyal
python tests/ziprecruiter/debug_ziprecruiter.py

# Test LinkedIn
python tests/linkedin/debug_linkedin.py

# Test Glassdoor
python tests/glassdoor/debug_glassdoor.py

# Test Google Jobs
python tests/google/debug_google.py
```

### **Environment Variables**
```bash
# Generic proxy settings
export PROXY_USER="your_username"
export PROXY_PASS="your_password"
export PROXY_HOST="proxy.example.com"
export PROXY_PORT="8080"

# iproyal residential proxies (for ZipRecruiter)
export IPROYAL_USER="your_iproyal_username"
export IPROYAL_PASS="your_iproyal_password"
```

## 📊 **Provider-Specific Notes**

### **Indeed**
- **Most restrictive** with parameter conflicts
- **Mobile approach** with iOS TLS fingerprinting
- **Search syntax matters** - use quotes and exclusions
- **IP blocking** is common - use residential proxies

### **ZipRecruiter**
- **Cloudflare protection** - uses CloudScraper
- **Works well** with iproyal residential proxies
- **Mobile headers** simulate iPhone app

### **LinkedIn**
- **Most aggressive** rate limiting (around page 10)
- **Desktop approach** works better
- **Proxies essential** for large-scale scraping

### **Glassdoor**
- **GraphQL API** with automatic CSRF token handling
- **Moderate** rate limiting
- **Desktop approach** 

### **Google Jobs**
- **Least restrictive** of all providers
- **Specific search syntax** required (`google_search_term`)
- **Copy terms** directly from Google Jobs website

## 🎯 **Best Practices**

1. **Start with debug scripts** to identify issues
2. **Use provider-specific search syntax**
3. **Respect parameter limitations** (especially Indeed)
4. **Use appropriate proxy strategy** for each provider
5. **Monitor rate limiting** and adjust accordingly
6. **Save results** to `tests/results/` for analysis 