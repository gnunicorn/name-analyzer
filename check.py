# -*- coding: utf-8 -*-

import urllib2, re

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


        print "%s\t%s (%d%%)\t\t%s (%d%%)" % (letter, cur_len, rel_cur,
                pop_len, rel_pop)

    return local_relatives, popular_relatives


def test():
    names = get_list_of_names()
    popular_names = most_popular_10_names_of_the_last_5_decades.split()
    intersected_count_wo = analyse(names, popular_names)
    names.add("Benjamin")
    print "*" * 20
    print "Now once again, adding ben...."
    print "*" * 20
    intersected_count_with = analyse(names, popular_names)
    pop_names = len(popular_names)
    percent_per_name = 100. / pop_names

    without_percent = intersected_count_wo * percent_per_name
    with_percent = intersected_count_with * percent_per_name
    increase = (100 / without_percent * with_percent) - 100
    print
    print
    print "Result - total Popularity"
    print "w/o Benjamin - with Benjamin"
    print "%s%% - %s%%" % (without_percent, with_percent)
    print "-----------------------------"
    print "%s%% =~ %s%% of your current popularity" % ((with_percent - without_percent), increase)
    print
    print "With 'Benjamin' you are %s%% more popular than you are now." %  increase
    print "You should hire him, he is a good investment!"


def graph_urls(local_relatives, popular_relatives):
    url = "http://chart.apis.google.com/chart?chs=900x200&chbh=a&chds=0,25&chco=4d89f9,C6D9fd&chd=t:%s|%s&cht=bvg&chl=a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z" % (','.join([str(x[0]) for x in popular_relatives]), ",".join([str(x[0]) for x in local_relatives]))

    print  "want a nice graph? Go here:", url
    local_relatives.sort()
    popular_relatives.sort()

    local_relatives.reverse()
    popular_relatives.reverse()

    url = "http://chart.apis.google.com/chart?chs=900x200&chbh=a&chds=0,25&chco=4d89f9,C6D9fd&chd=t:%s|%s&cht=bvg" % (','.join([str(x[0]) for x in popular_relatives]), ",".join([str(x[0]) for x in local_relatives]))
    print  "want to see the ...", url


def analyse(names, popular_names):
    #names.append("Ben")
    local_count = len(names)
    names_by_letter = sort_names(names)

    popular_count = len(popular_names)
    popular_by_letter = sort_names(popular_names)

    print "L\tlocal\t\tgermany wide"
    local, popular = small_analyzis(names_by_letter, popular_by_letter,
            local_count, popular_count)

    graph_urls(local, popular)

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

    local, popular = small_analyzis(intersected_by_letter, popular_by_letter,
            intersected_count, popular_count)

    graph_urls(local, popular)

    return intersected_count



