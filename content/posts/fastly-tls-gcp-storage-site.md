---
title: "Hugo Generated, Google Cloud Storage Hosted, Static Site Behind Fastly"
author: "Colton J. McCurdy"
type: ""
date: 2020-03-04
subtitle: ""
image: ""
tags: ["website", "2020", "fastly", "google-compute-platform", "google-cloud-storage"]
---

_Full disclosure, I am employed by Fastly. However, I was not asked or paid by Fastly
to write this post. This post has no affiliation with my employment at Fastly._

If you want to skip the background section and jump straight to the step-by-step
guide, [click here](#process-overview).

## Background

### Is this the Right Post for You?

This post is _not_ the quickest way to host a static site, for that, I would strongly
recommend Netlify. To read more about hosting a Hugo-generated static site on Netlify,
check out [this guide](https://gohugo.io/hosting-and-deployment/hosting-on-netlify/).

In regards to [Google Cloud Storage (GCS)](https://cloud.google.com/storage), this
guide will _not_ be the minimal steps necessary to get up an running. If you are
interested in the minimal steps necessary for hosting your static site on GCS,
check out [this guide](https://cloud.google.com/storage/docs/hosting-static-website).

This post also _does not_ guide you through the easiest way to add [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security)
or get up and running with [Fastly as a Content Delivery Network (CDN)](https://www.fastly.com/products/cdn).
If you are only interested in TLS or testing out Fastly with a GCS backend, check
out [this guide](https://cloud.google.com/load-balancing/docs/https/adding-backend-buckets-to-load-balancers)
or [this guide](https://docs.fastly.com/en/guides/google-cloud-storage), respectively.

Rather, this post documents the process that I followed for the configuration that
I am interested in for this site (i.e., `www.mccurdyc.dev`).

### `.dev` top-level domain (tld)

Google mentions a few reasons why you would want to use a .dev tld, [here](https://get.dev/#benefits).
The two reasons that I am interested in a `.dev` domain, namely `mccurdyc.dev`, are
because it encourages security and because it's "cool".
`.dev` ecourages --- actually forces --- security by being included on the HTTP
Strict Transport Security (HSTS) Preload list which enforces the use of Transport
Layer Security (TLS) in web browsers.

_To read more about HSTS and HSTS Preloading check out the following posts by
the respected Security Researcher, Scott Helme._

+ [HSTS - The missing link in Transport Layer Security](https://scotthelme.co.uk/hsts-the-missing-link-in-tls/)
+ [HSTS Preloading](https://scotthelme.co.uk/hsts-preloading/)

However, because `.dev` tlds are on the HSTS Preload list, it makes it slightly
more difficult to use GCS than described in Google's ["Hosting a static
site" documentation](https://cloud.google.com/storage/docs/hosting-static-website).
In Google's documentation they tell you to create a `CNAME` record pointed at
`c.storage.googleapis.com.`. This will not work. Instead, read what I did below to
solve this issue. The short answer is [this](https://cloud.google.com/storage/docs/troubleshooting#https).

### Deploying `mccurdyc.dev`

Right now, there is some terraform for provisioning the GCS bucket and the rest
is also very manual, consisting of building the static site with `hugo` and then
running `hugo deploy` to push the assets to the GCS bucket. I hope to improve and
document this process in the future. I will most likely use Google Cloud Build,
similar to what is described in [this post](https://www.realjenius.com/2019/11/25/cloudbuild-hugo-gcs/).

### Motivations

Why did I choose Hugo? Why did I choose to not use Netlify? Why did I choose Google Cloud Platform (GCP)
over Amazon Web Services (AWS)? Why did I choose Fastly?

I chose Hugo because it is written in the programming language that I am most comfortable
with and therefore effectively able to contribute back to. Additionally, the site
build times are extremely fast. I chose to go the more tedious and manual route and
avoid Netlify because I am interested in learning what all is involved in deploying
a static site. Also, because I want more control. GCP over AWS because I used
AWS at my day job and wanted to familiarize myself with the competing platform.
Fastly, again because we used a competing platform at my previous day job and I
am about to start working at Fastly and I wanted to familiarize myself with the product.

---

## Process Overview

There were a few main parts to put `mccurdyc.dev` behind Fastly.

1. [Hugo Builds and Deployments](#hugo-builds-and-deployments)
2. Google Cloud Platform (GCP) / Google Cloud Storage (GCS) Configuration
    1. Create a Project on GCP
    2. Create a GCS "Website Bucket"
    3. Create an HTTPS Load Balancer
3. Create a Fastly Service
    1. Configure an Origin Host
    2. Force TLS and HSTS
    3. Fastly HTTPS and Network Configuration
4. Fastly Shared and Procured TLS Configuration (**paid**)
    1. Create a TLS domain
5. Domain Name System (DNS) Provider Configuration

### Hugo Builds and Deployments

_Creating a static site with Hugo is out of the scope of this post. Refer to the
[Quickstart Guide](https://gohugo.io/getting-started/quick-start/) in Hugo's documentation._

One component that is important and related to both Hugo and this post is deploying
to GCS. Hugo has documentation on their site for [deploying to GCS](https://gohugo.io/hosting-and-deployment/hugo-deploy/).
For `mccurdyc.dev`, I have added the following to the `config.toml` file in the root
of my Hugo project.

```toml
[deployment]
[[deployment.targets]]
name = "www"
URL = "gs://www.mccurdyc.dev"
```

Before being able to deploy, you will need to install the [`gcloud` cli tool](https://cloud.google.com/sdk/gcloud)
and login with `gcloud auth login`.

Then, the plain `hugo` command, by default, creates a `public/` directory, which
gets deployed to GCS with `hugo deploy`.

### Google Cloud Platform (GCP) / Google Cloud Storage (GCS) Configuration

While primarily documenting how to configure your Fastly Service, rather than GCS specifically,
it is helpful to reference the documentation on [using GCS as an origin server](https://docs.fastly.com/en/guides/google-cloud-storage).

_Note: Originally, I configured everything around using `www.mccurdyc.dev` because
this is what GCP recommended for [hosting a static website in a GCS bucket](https://cloud.google.com/storage/docs/hosting-static-website).
For more information on using GCS for a static website, check out
[this document on static website examples and tips](https://cloud.google.com/storage/docs/static-website)._

1. Create a GCP Project

_The details for creating a GCP project are out of the scope of this post. Refer
to this document on [Creating and Managing Projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects)._

I find it easier to create resources in the console first and tweak them there and
then do a `terraform import` of the resource and check the difference between
the resource definition that I have locally and the state of the resource with
`terraform plan`. The documentation for defining a Google Project in Terraform
can be found [here](https://www.terraform.io/docs/providers/google/r/google_project.html).

The Terraform commands that I ran were as follows:

0. `terraform init`
1. `terraform import google_project.mccurdyc_dot_dev daring-octane-268913`
2. `terraform import google_service_account.create_access_service_account projects/daring-octane-268913/serviceAccounts/create-access@daring-octane-268913.iam.gserviceaccount.com`

While the terraform specifies that the bucket

https://cloud.google.com/storage/docs/xml-api/put-bucket-website

> Note: A bucket's website configuration only applies to requests that use either the CNAME redirect endpoint or Cloud Load Balancing.

### Create a "Service" on Fastly
  1. Configure origin host
  2. Force TLS and HSTS

### Fastly service configuration

1. Create a TLS domain for communication between clients and Fastly
2. Create a TLS domain for communication between Fastly and the origin server

### Fastly HTTPS and network configuration

[Fastly Free TLS](https://docs.fastly.com/en/guides/setting-up-free-tls)
> When using free TLS, you **cannot DNS alias** your own domain (for example, `www.example.org`)
to the shared domain. If you do, a TLS name mismatch warning will appear in the browser.
The only way to avoid the mismatch error is to order a paid TLS option.

_Adding HTTPS to your domain is super easy, but does require that you attach a credit
card to your Fastly account and upgrade from the free tier._

It's important that the domain entered in Fastly's console matches the domain in your
domain registrar. For example, I use `mccurdyc.dev`, while a lot of the configuration
in Fastly uses `www.mccurdyc.dev`, the TLS configuration in Fastly also needs to be `mccurdyc.dev`.

After upgrading your account and enabling HTTPS, you will need to add a `CNAME`
and `TXT` DNS records in your domain registrar.

_You can always check that DNS records have been updated with a command like
`dig www.mccurdyc.dev`. I found [this resource](https://mediatemple.net/community/products/dv/204644130/understanding-the-dig-command)
helpful for finding example usage of the `dig` command._

### Domain Name System (DNS) configuration

_**Don't** get confused here and do what I originally did, which was to also follow
the [GCS bucket static website guide](https://cloud.google.com/storage/docs/hosting-static-website).
This guide suggests naming your bucket something like `www.mccurdyc.dev`, creating
a `CNAME` record and verifying your domain name. You shouldn't need to do these things
since we are configuring DNS to point to Fastly, which points to the GCS bucket._

1. `TXT` DNS record for Fastly TLS verification
2. `www` `CNAME` record pointed at [Fastly's TLS-enabled hostnames](https://docs.fastly.com/en/guides/adding-cname-records#tls-enabled-hostnames)

![Permanent redirects]()
![Custom resource records]()

_DNS caching can be annoying when chaning things frequently, especially with a
long cache TTL. So, again, you can use `dig www.mccurdyc.dev +short` to watch for
the DNS `CNAME` record change to go through. [Checking your `CNAME` record](https://docs.fastly.com/en/guides/adding-cname-records#checking-your-cname-record)._

---

## Other Notes / "Gotchas"

I ran into an issue where my terraform state wouldn't `force_destroy` my created
bucket. I had to manually edit my `tfstate` file. https://github.com/terraform-providers/terraform-provider-google/issues/1509
I wanted to rename my bucket from `mccurdyc.dev` to `www.mccurdyc.dev` because
Fastly doesn't recommend using [apex domain names](https://www.quora.com/What-is-an-apex-domain).

### Using an Apex Domain with Fastly

This is due to routing benefits when you don't choose to use an apex domain, however,
you can still [use Fastly with an apex domain](https://docs.fastly.com/en/guides/using-fastly-with-apex-domains).

### Fastly TLS Resources

1. [Fastly TLS](https://docs.fastly.com/products/tls-service-options#fastly-tls)
2. [Fastly Managed certificates](https://docs.fastly.com/en/guides/serving-https-traffic-using-fastly-managed-certificates)
3. [Setting up TLS for a domain](https://docs.fastly.com/en/guides/serving-https-traffic-using-fastly-managed-certificates#setting-up-tls-for-a-domain)
4. [NET::ERR_CERT_COMMON_NAME_INVALID error](https://docs.fastly.com/en/guides/tls-certificate-errors)
5. [Managing domains on TLS certificates](https://docs.fastly.com/en/guides/managing-domains-on-tls-certificates)
6. [Updating the `CNAME` record with your DNS provider](https://docs.fastly.com/en/guides/adding-cname-records#updating-the-cname-record-with-your-dns-provider)
7. [`Error 503 hostname doesn't match against certificate`](https://docs.fastly.com/en/guides/common-503-errors#error-503-hostname-doesnt-match-against-certificate)
  This was specifically for the encrypted communication between Fastly and Google Cloud Storage
  1. Create another Fastly-manage certificate for `www.mccurdyc.dev.storage.googleapis.com`
  2. Verify ownership of `www.mccurdyc.dev.storage.googleapis.com` by uploading a `.txt` file to `/.well-known/pki-validation/gsdv.txt`
  3. Verify access to the file by browsing `http://www.mccurdyc.dev.storage.googleapis.com/.well-known/pki-validation/gsdv.txt`

### Questions for Fastly

1. Is it possible to create a public "Sample Service" so that customers could browse
around in the Sample Service and check out the configuration.
2. issue with "Shared and procured TLS" using `www.mccurdyc.dev.storage.googleapis.com` works fine with `mccurdyc-dot-dev.storage.googleapis.com`

## Resources

+ HTTPS GCS
  + [Full HTTPS load balancer example with a VPC](https://cloud.google.com/load-balancing/docs/https/https-load-balancer-example)
  + [Adding backend buckets to load balancers](https://cloud.google.com/load-balancing/docs/https/adding-backend-buckets-to-load-balancers)
  + [External HTTP(S) Load Balancing overview](https://cloud.google.com/load-balancing/docs/https)
  + [Using Google-managed SSL certificates](https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs)
  + [SSL certificates overview](https://cloud.google.com/load-balancing/docs/ssl-certificates)
