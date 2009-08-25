# -*- coding: utf-8 -*-



import urllib2
import re
import time
import os

from genshi.template import TemplateLoader
loader=TemplateLoader(os.path.dirname(__file__), auto_reload=True)

# all the 10 most popular names of the last 5 decades. take from:
#   http://www.gfds.de/vornamen/beliebteste-vornamen/
# slightly cleaned up
most_popular_10_names_of_the_last_5_decades = u"""Andrea
Angelika
Anja
Anke
Anna
Annett
Antje
Barbara
Birgit
Brigitte
Christin
Christina
Claudia
Daniela
Diana
Doreen
Franziska
Gabriele
Heike
Ines
Jana
Janina
Jennifer
Jessica
Julia
Juliane
Karin
Karolin
Katharina
Kathrin
Katja
Kerstin
Klaudia
Kristin
Laura
Lea
Lena
Lisa
Mandy
Manuela
Maria
Marie
Marina
Martina
Melanie
Monika
Nadine
Nicole
Petra
Sabine
Sabrina
Sandra
Sara
Silke
Simone
Sophia
Stefanie
Susanne
Tanja
Ulrike
Ursula
Uta
Vanessa
Yvonne 	
Alexander
Andreas
Benjamin
Bernd
Christian
Daniel
David
Dennis
Dieter
Dirk
Dominik
Eric
Felix
Florian
Frank
Jan
Jens
Jonas
Jörg
Jürgen
Kevin
Klaus
Kristian
Leon
Lukas
Marcel
Marco
Mario
Markus
Martin
Mathias
Max
Maximilian
Michael
Mike
Niklas
Patrick
Paul
Peter
Philipp
Ralf
René
Robert
Sebastian
Stefan
Steffen
Sven
Thomas
Thorsten
Tim
Tobias
Tom
Ulrich
Uwe
Wolfgang 
"""

def get_list_of_names():
    # reading the header I know that you are utf-8. Might has to be made
    # dynamic later but for now hard-coding should just work.
    return set([x for x in re.findall("\<span\>(.*?)\<\/span\>",
            urllib2.urlopen("http://www.ableton.com/about-ableton").read()) ])

def sort_names(names):
    results = dict()
    for name in names:
        letter = name[0].lower()
        try:
            results[letter].append(name)
        except KeyError:
            results.setdefault(letter, []).append(name)

    for key, names in results.iteritems():
        names.sort()
    return results

def small_analyzis(names_by_letter, popular_by_letter, local_count, popular_count):

    a_local_percent = 100. / local_count
    a_popular_percent = 100. / popular_count

    popular_relatives = []
    local_relatives = []

    res = []
    for letter in "abcdefghijklmnopqrstuvwxyz":
        try:
            current = names_by_letter[letter]
        except KeyError:
            current = []

        try:
            popular = popular_by_letter[letter]
        except KeyError:
            popular = []

        cur_len = len(current)
        pop_len = len(popular)

        rel_cur = cur_len * a_local_percent
        rel_pop = pop_len * a_popular_percent

        local_relatives.append((rel_cur, letter))
        popular_relatives.append((rel_pop, letter))


        res.append("%s\t%s (%d%%)\t\t%s (%d%%)" % (letter, cur_len, rel_cur,
                pop_len, rel_pop))

    return res, local_relatives, popular_relatives

def render(name, context):
    tmpl = loader.load(name)
    return tmpl.generate(**context).render('html', doctype='html')


def full_check(name, sleep_time):
    try:
        os.mkdir(name)
    except OSError:
        print "Maybe you already did a report for this name, didn't you?"
        raise
    print "receiving list of names"
    time.sleep(sleep_time)

    names = get_list_of_names()

    print "reading popular names from the last 5 decades"
    time.sleep(sleep_time)

    popular_names = most_popular_10_names_of_the_last_5_decades.split()

    print "direct analysis"
    time.sleep(sleep_time * 4)

    prefix = os.path.join(name, 'without')
    intersected_count_wo, res_without, res_without_inter = \
            analyse(names, popular_names, prefix)

    print
    print "*" * 20
    print "Analyzing again, this time including '%s'...." % name
    print "*" * 20
    time.sleep(sleep_time * 6)

    prefix = os.path.join(name, 'with')
    names.add(name)
    intersected_count_with, res_with, res_with_inter = \
            analyse(names, popular_names, prefix)
    pop_names = len(popular_names)
    percent_per_name = 100. / pop_names

    without_percent = intersected_count_wo * percent_per_name
    with_percent = intersected_count_with * percent_per_name
    increase = (100 / without_percent * with_percent) - 100

    print
    print "calculating end results"
    time.sleep(sleep_time * 4)

    result_url = "http://chart.apis.google.com/chart?chs=250x150&chtt=Popularity+without+and|with+%s&chbh=a&chds=%d,%d&chd=t:%s,%s&cht=gom" % (name, without_percent - 1, with_percent + 1, without_percent, with_percent)
    download_to_file(result_url, os.path.join(name, 'result.png'))

    print "Calculating advice.."

    time.sleep(sleep_time * 4)
    advice = "Doesn't actually matter..."
    if increase < 0.5:
        advice = "Do nothing. It is not worth the trouble."
    elif increase <= 1:
        advice = "Ask him to do an internship."
    elif increase <= 2:
        advice = "Sounds about alright. Make some tests of his skills."
    elif increase <= 3:
        advice = "Uh.. that is good one, you should consider hireing him."
    elif increase <= 4:
        advice = "You should hire him, he is a good investment!"
    else:
        advice = "DUDE... WHAT ARE YOU WAITING FOR?"

    context = {
            'name': name,
            'advice': advice,
            'with_percent': with_percent,
            'without_percent': without_percent,
            'res_with': res_with,
            'res_with_inter': res_with_inter,
            'res_without': res_without,
            'res_without_inter': res_without_inter,
            'increase': increase}

    path = os.path.join(name, 'index.html')

    to_save = open(path, 'w')
    to_save.write(render('template.html', context))
    to_save.close()
    print "Report done. Look into %s please." % path

def graph_urls(local_relatives, popular_relatives, prefix=""):
    unsorted_url = "http://chart.apis.google.com/chart?chs=900x200&chbh=a&chds=0,25&chco=4d89f9,C6D9fd&chd=t:%s|%s&cht=bvg&chl=a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z" % (','.join([str(x[0]) for x in popular_relatives]), ",".join([str(x[0]) for x in local_relatives]))

    local_relatives.sort()
    popular_relatives.sort()

    local_relatives.reverse()
    popular_relatives.reverse()

    sorted_url = "http://chart.apis.google.com/chart?chs=900x200&chbh=a&chds=0,25&chco=4d89f9,C6D9fd&chd=t:%s|%s&cht=bvg" % (','.join([str(x[0]) for x in popular_relatives]), ",".join([str(x[0]) for x in local_relatives]))
    return unsorted_url, sorted_url

def download_to_file(url, filename):
    to_save = open(filename, 'wb')
    try:
        to_save.write(urllib2.urlopen(url).read())
    finally:
        to_save.close()

def analyse(names, popular_names, prefix):
    #names.append("Ben")
    local_count = len(names)
    names_by_letter = sort_names(names)

    popular_count = len(popular_names)
    popular_by_letter = sort_names(popular_names)

    print "Analyzing"
    res, local, popular = small_analyzis(names_by_letter, popular_by_letter,
            local_count, popular_count)

    unsorted_url, sorted_url = graph_urls(local, popular)
    print "downloading graphs"
    download_to_file(unsorted_url, '%s_unsorted.png' % prefix)
    download_to_file(sorted_url, '%s_sorted.png' % prefix)
    print "done"


    print "analyzing intersection .........."

    intersected_by_letter = {}
    intersected_count = 0
    for letter, names in names_by_letter.iteritems():
        try:
            inter = set(names).intersection(set(popular_by_letter[letter]))
            intersected_count += len(inter)
            intersected_by_letter[letter] = inter
        except KeyError:
            intersected_by_letter[letter] = []

    print "Number of matches", intersected_count

    res_inter, local, popular = small_analyzis(intersected_by_letter,
            popular_by_letter, intersected_count, popular_count)

    unsorted_url, sorted_url = graph_urls(local, popular)
    print "downloading graphs"
    download_to_file(unsorted_url, '%s_inter_unsorted.png' % prefix)
    download_to_file(sorted_url, '%s_inter_sorted.png' % prefix)
    print "done"

    return intersected_count, res, res_inter

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print "Please provide a name as the first and only parameter"
        sys.exit(1)

    name = sys.argv[1]
    print "Checking", name
    full_check(name, 0.)

