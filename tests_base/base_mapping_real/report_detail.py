import json
import math

from lib import util

percent = util.percent


def generateMappingQualityPlot(self, page):
	results = self.getRunResults()

	columns = [["Mapped"]]

	csv = "mapq_threshold,mapped_reads\n"

	correct = []
	wrong = []
	mc = max(1, float(results.total))
	mw = max(1, float(results.total))

	wrong_scale = float(results.correct / mc) / float((1 + results.wrong) / mw)

	mapqs = sorted(results.mapq_cumulated)
	for curr in mapqs:
		columns[0].append(results.mapq_cumulated[curr]["correct"] / float(mc))
		csv += "%d,%d\n" % (curr,results.mapq_cumulated[curr]["correct"])

	csv_filename = self.writeCSV(self.getMapper().getName() + "_mapqs",csv)

	page.addSection("Mapping Quality Thresholds", """<div id="plot_mapq_tresh"></div>%s""" % util.makeExportDropdown("plot_mapq_thresh",csv_filename), None, "The plot below shows the percentages of mapped reads for all mapping quality thresholds for this mapper. The values at threshold 0 therefore correspond to the unfiltered results.")
	page.addScript("""
var cols=%s;
var a=0;
var b=0;
var last_a=0;
var last_b=0;

function updateRange()
{
	if(last_a==a && last_b==b)
	{
		setTimeout(updateRange,500);
		return;
	}
 
        an=Math.floor(parseInt(a));
        bn=Math.floor(parseInt(b));
	var mn = 0;
	var mx = 0;
	for(i=an;i<bn;i++)
	{
		mx=Math.max(mx,cols[0][i+1]);
		mn=Math.min(mn,cols[1][i+1]);
	}
	r={}
	r.max=mx;
	r.min=mn;
	chart.axis.range(r);
	last_a=a;
	last_b=b;
	setTimeout(updateRange,500);
}
setTimeout(updateRange,500);

var chart = c3.generate({
bindto: '#plot_mapq_tresh',
data: {
  columns: %s,
  type: "area"
},
grid: {
  y: {
    show: true
  }
},
axis: {
  x: {
    label: "Mapping Quality Threshold"
  },

  y: {
    label: { text: "Read Count", position: "outer-middle" },
    tick: {
       format: function(v) { if(v>=0){return Math.min(100,(Math.round(100000*v)/1000))+"%%";}else{ return Math.min(100,(Math.round(100000*(-v/%f))/1000))+"%%";} }
    }
  }
},
legend: {
	position: "right"
},
subchart: {
	show: true,
	onbrush: function (d) {
		a = d[0];
		b = d[1];
	}
}
});""" % (json.dumps(columns), json.dumps(columns), wrong_scale))


def report_detail(self, gen, page):
	stats = self.getRunResults()

	if stats == None:
		return

	generateMappingQualityPlot(self, page)

	html = ""
	html += "<div class=\"table-responsive\"><table class=\"table table-striped\">"
	html += "<tbody>"
	html += "<tr><th class=\"col-md-6\">Mapped</th>"
	html += "<td class=\"col-md-2\">%s</td>" % str(stats.correct)
	html += "<td class=\"col-md-2\">%s</td>" % percent(stats.correct, stats.total)
	html += "</tr><tr><th>Not Mapped</th>"
	html += "<td>%s</td>" % str(stats.not_mapped+stats.not_found)
	html += "<td>%s</td>" % percent(stats.not_mapped+stats.not_found, stats.total)
	html += "</tr><tr><th>Total</th>"
	html += "<td>%s</td>" % str(stats.total)
	html += "<td>%s</td>" % percent(stats.total, stats.total)
	html += "</tbody>"
	html += "</table></div>"
	page.addSection("Basic Statistics", html)

	html = ""
	html += "<div class=\"table-responsive\"><table class=\"table table-striped\">"
	html += "<tbody>"
	html += "<tr><th class=\"col-md-6\">Not mapped</th>"
	html += "<td class=\"col-md-2\">%s</td>" % str(stats.not_mapped)
	html += "<td class=\"col-md-2\">%s</td>" % percent(stats.not_mapped, stats.total)
	html += "</tr><tr><th>Missing in mapper output</th>"
	html += "<td>%s</td>" % str(stats.not_found)
	html += "<td>%s</td>" % percent(stats.not_found, stats.total)
	html += "</tr>"
	html += "</tbody>"
	html += "</table></div>"
	page.addSection("Read Failure Statistics", html)

	results = self.getRunResults()
	if results == None:
		return

	html = ""
	html += "<div class=\"table-responsive\"><table class=\"table table-striped\">"
	html += "<tbody>"
	html += "<tr><th class=\"col-md-6\">Secondary Alignments</th><td class=\"col-md-4\">%s</td></tr>" % str(stats.ignored_testee)
	html += "</tbody>"
	html += "</table></div>"
	page.addSection("Advanced Statistics", html)

	html = ""
	html += "<div class=\"table-responsive\"><table class=\"table table-striped\">"
	html += "<tbody>"
	html += "<tr><th class=\"col-md-6\">Raw Mapping Time</th><td class=\"col-md-4\">%.3fs</td></tr>" % results.maptime_raw
	html += "<tr><th>Effective Mapping Time</th><td>%.3fs</td></tr>" % results.maptime
	html += "<tr><th>Effective Init Time</th><td>%.3fs</td></tr>" % results.inittime
	html += "<tr><th>Effective Time Measure</th><td>%s</td></tr>" % results.time_measure
	
	html += "<tr><th>Mapping Time (Wall)</th><td>%.3fs</td></tr>" % results.walltime
	html += "<tr><th>Mapping Time (CPU)</th><td>%.3fs</td></tr>" % results.cputime
	html += "<tr><th>Mapping Time (CPU User)</th><td>%.3fs</td></tr>" % results.usrtime
	html += "<tr><th>Mapping Time (CPU System)</th><td>%.3fs</td></tr>" % results.systime

	html += "<tr><th>Init Time (Wall)</th><td>%.3fs</td></tr>" % results.initwalltime
	html += "<tr><th>Init Time (CPU)</th><td>%.3fs</td></tr>" % results.initcputime
	html += "<tr><th>Init Time (CPU User)</th><td>%.3fs</td></tr>" % results.initusrtime
	html += "<tr><th>Init Time (CPU System)</th><td>%.3fs</td></tr>" % results.initsystime
	html += "</tbody>"
	html += "</table></div>"
	page.addSection("Timing", html)

	html = ""
	html += "<div class=\"table-responsive\"><table class=\"table table-striped\">"
	html += "<tbody>"
	html += "<tr><th class=\"col-md-6\">Mapper Memory Usage</th><td class=\"col-md-4\">%d MB</td></tr>" % (results.memory / 1000000)
	html += "<tr><th>Total Test Runtime (Wall)</th><td>%.3fs</td></tr>" % self.getRunTime()
	html += "<tr><th>Mapper Command Line:</th><td>&nbsp;</td></tr><tr><td colspan=2>%s</td></tr>" % (
	self.getMapper().getCommandLineMain())
	html += "</tbody>"
	html += "</table></div>"
	page.addSection("Additional Information", html)

	return html
