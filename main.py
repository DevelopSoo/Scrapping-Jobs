"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import Flask, render_template, request, send_file, redirect, send_file
from scrapper import scrape_wework, scrape_SO, scrape_remote
from exporter import save_to_file




app = Flask("Remote Jobs")

db = {}

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/search")
def search():
  term = request.args.get("term")
  if term:
    term = term.lower()
    fromDb = db.get(term)
    if fromDb:
      all_jobs = fromDb
    else:
      wework_jobs = scrape_wework(term)
      # wework_number = len(wework_jobs)
      
      remote_jobs = scrape_remote(term)
      # remote_number = len(remote_jobs)

      SO_jobs = scrape_SO(term)
      # SO_number = len(SO_jobs)
      all_jobs   = wework_jobs+remote_jobs+SO_jobs
      db[term]=all_jobs

  # return render_template("search.html", term = term, wework_jobs = wework_jobs, remote_jobs = remote_jobs, SO_jobs = SO_jobs, number= len(all_jobs))
  return render_template("search.html", term = term, all_jobs = all_jobs, number= len(all_jobs))

@app.route("/export")
def export():
  try:
    term = request.args.get("term")
    if not term:
      raise Exception()
    term = term.lower()
    all_jobs = db.get(term)
    if not all_jobs:
      raise Exception()
    save_to_file(all_jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")


app.run(host="0.0.0.0")

