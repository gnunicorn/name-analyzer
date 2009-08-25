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
Jungennamen
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
    return re.findall("\<span\>(.*?)\<\/span\>",
            urllib2.urlopen("http://www.ableton.com/about-ableton").read())


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


def test():
    names = get_list_of_names()
    #names.append("Ben")
    local_count = len(names)
    names_by_letter = sort_names(names)

    popular_names = most_popular_10_names_of_the_last_5_decades.split()
    popular_count = len(popular_names)
    popular_by_letter = sort_names(popular_names)

    print "L\tlocal\t\tgermany wide\t\tadvice"

    a_local_percent = local_count / 100.
    a_popular_percent = popular_count / 100.

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


        advice = ''

        print "%s\t%s (%s%%)\t\t%s (%s%%)\t\t%s" % (letter, cur_len, rel_cur,
                pop_len, rel_pop, advice)

    local_relatives.sort()
    popular_relatives.sort()

    local_relatives.reverse()
    popular_relatives.reverse()

    print "so the order should be:\n", " ".join([x[1] for x in popular_relatives if x[0] > 0])
    print "but here it is:\n", " ".join([x[1] for x in local_relatives if x[0] > 0])

