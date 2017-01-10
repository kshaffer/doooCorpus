#  -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import sys
import subprocess
import datetime
import codecs
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
import csv

def write_csv(data, filename):
    with open(filename, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)

def write_to_file(filename, data):
    f = open(filename, 'wb')
    f.write(data)
    f.close()

url_list = ['http://jeremydean.org/blog/getting-started/an-annotated-domain-of-ones-own/', 'https://www.edsurge.com/news/2015-12-18-byu-s-bold-plan-to-give-students-control-of-their-data', 'http://bavatuesdays.com/a-domain-of-ones-own/', 'http://er.educause.edu/articles/2009/9/a-personal-cyberinfrastructure', 'https://blog.timowens.io/a-domain-of-ones-own-rebooted/', 'https://www.insidehighered.com/blogs/hack-higher-education/top-ed-tech-trends-2012-data-and-learning-analytics', 'http://www.wired.com/insights/2012/07/a-domain-of-ones-own/', 'http://bavatuesdays.com/documenting-a-domain-of-ones-own/', 'https://larrymccallum.wordpress.com/2012/12/11/a-domain-of-ones-own/', 'http://bavatuesdays.com/babyboomers-eat-babies-or-a-weak-critique-of-domain-of-ones-own/', 'http://chronicle.com/blogs/techtherapy/2012/12/05/episode-101-giving-everyone-at-college-a-domain-of-ones-own/', 'http://www.downes.ca/post/59607', 'https://blog.timowens.io/building-a-domain-of-ones-own-hosting/', 'https://blog.timowens.io/building-a-domain-of-ones-own-the-panel/', 'https://blog.timowens.io/building-a-domain-of-ones-own-the-sign-up/', 'https://blog.timowens.io/building-a-domain-of-ones-own-plugins-add-ons-and-plans/', 'http://www.zachwhalen.net/posts/a-reflection-on-teaching-with-umwdomains/', 'http://www.umw.edu/greatminds/2013/02/11/at-home-on-the-web/', 'https://blog.timowens.io/varying-degrees-of-open/', 'https://blog.timowens.io/building-a-syndication-framework-for-the-domain-of-ones-own/', 'https://blog.timowens.io/unified-syndication-of-a-domain-of-ones-own/', 'https://thebluereview.org/beyond-disruption/', 'https://blog.timowens.io/redefining-reclaim-efforts/', 'https://blog.timowens.io/a-distributed-domain-of-ones-own/', 'http://www.umw.edu/news/2013/08/13/umw-freshmen-build-digital-identities-through-innovative-project/', 'http://chronicle.com/blogs/profhacker/teaching-a-domain-of-ones-own-with-reclaim-hosting/52279', 'http://www.cplong.org/2013/10/a-domain-of-your-own/', 'https://blog.timowens.io/building-a-community-from-umw-domains/', 'https://www.davidson.edu/news/news-stories/131213-mellon-foundation-digital-studies-award', 'http://www.marybecelia.com/uncategorized/new-year-fresh-start/', 'http://www.digitalpedagogylab.com/hybridped/building-community-critical-literacies-domain-ones-incubator/', 'http://www.profdavehenderson.com/uncategorized/what-i-learned-from-the-domain-of-ones-own-program/', 'https://campustechnology.com/articles/2014/04/02/an-e-portfolio-with-no-limits.aspx', 'https://sites.duke.edu/digitalwritingandpedagogylab/speakers/', 'http://hackeducation.com/2014/04/25/domain-of-ones-own-incubator-emory', 'http://ewprogram.com/incubator/', 'http://at.blogs.wm.edu/opening-up-the-web-for-students-and-faculty/', 'http://www.mgregory.org/part-play/domain-of-ones-own-debrief/', 'http://www.mdsnd.net/debrief/debrief-1-domain-of-ones-own/', 'http://domainnamewire.com/2014/12/23/interesting-a-domain-of-ones-own-at-university-of-mary-washington/', 'http://gettingsmart.com/2014/12/encourage-writing-domain-blog-portfolio/', 'https://blog.timowens.io/making-the-web-we-want/', 'http://digital.anthro-seminars.net/admin/davidson-domains/', 'http://teacherlytech.net/?p=472', 'http://blogs.edweek.org/edweek/on_innovation/2015/02/its_time_for_students_to_own_the_student_record_b2c_lms_compansion.html', 'http://carrieschroeder.com/tigerdomains.html', 'http://dml2015.dmlhub.net/event/12569-panel-ol-domains-of-their-own-piloting-personal-cyber-infrastructure-projects-at-four-disparate-campuses/', 'http://mfeldstein.com/the-educause-ngdle-and-an-api-of-ones-own/', 'http://www.downes.ca/post/64075', 'http://brocansky.com/2015/06/reflections-on-teaching-in-the-public-web/', 'http://edtechcurmudgeon.blogspot.com/2015/06/ci-keys-defending-pilot-questioning.html', 'http://jleafstedt.com/uncatergorized/connected-learning-spaces-with-ci-keys/', 'http://www.johnastewart.org/dh/ou-create/', 'https://medium.com/bright/the-web-we-need-to-give-students-311d97713713#.2ykccqiyr', 'http://adamcroom.com/2015/08/domains-now-available-campus-wide/', 'http://chronicle.com/blogs/profhacker/starting-your-own-website-reclaim-your-hosting/60939', 'http://www.samplereality.com/2015/09/13/what-are-the-bottlenecks-of-davidson-domains/', 'http://bavatuesdays.com/digital-pedagogy-empowered-choice-and-personal-domains/', 'http://hjhether.com/blog/2015/09/24/launching-tiger-domains-pilot-project/', 'https://literatecomputing.com/t/a-domain-of-ones-own/1677', 'http://andrearehn.com/blog/launching-whittier-domains/', 'http://katefarley.org/checking-in/', 'http://byuocio.tumblr.com/post/137583594259/aspen-grove-winter-workshop-2016', 'http://diglibarts.whittier.edu/environmental-science-students-build-website/', 'https://blog.goreact.com/giving-power-back-to-the-people-well-the-students/', 'http://litanalysis.suzannechurchill.com/s16/2016/05/06/isabelles-davidson-domains/', 'http://blog.mahabali.me/blog/educational-technology-2/i-dont-own-my-domain-i-rent-it-dooo/', 'http://hackeducation.com/2016/08/23/domains', 'http://www.cal.msu.edu/news/webhostingservice?utm_content=buffer02700&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer', 'http://musicfordeckchairs.com/blog/2016/09/06/for-now-our-own/', 'http://bavatuesdays.com/domains-of-online-scholarly-presence/', 'http://bavatuesdays.com/practical-advice-for-running-domain-of-ones-own/', 'http://bavatuesdays.com/domain-of-ones-own-and-wordpress-networks/', 'http://bavatuesdays.com/a-subdomain-of-ones-own-with-potential/', 'http://bavatuesdays.com/domain-of-ones-own-2-0-the-manatee-release/', 'http://bavatuesdays.com/considering-running-domain-of-ones-own-on-your-campus/', 'http://bavatuesdays.com/domain-of-ones-own-as-limitless-as-the-web/', 'http://bavatuesdays.com/domain-of-ones-own-is-all-business/', 'http://bavatuesdays.com/domain-of-ones-own-presentation-at-tedxusagradocorazon/', 'http://bavatuesdays.com/domain-of-ones-own-notes-from-the-trailing-edge/', 'http://bavatuesdays.com/domain-of-ones-own-a-toolkit-for-user-innovation/', 'http://bavatuesdays.com/the-long-history-of-domain-of-ones-own/', 'http://bavatuesdays.com/domain-of-ones-own-digital-liberal-arts-and-the-popular-imagination/', 'http://bavatuesdays.com/domain-of-ones-own-poster-visualizing-the-connections/', 'http://bavatuesdays.com/domain-of-ones-own-the-most-fantasmagorical-concept-in-the-history-of-everthing/', 'http://bavatuesdays.com/domain-of-ones-own-poster-now-riffed-with-animation/', 'http://bavatuesdays.com/domain-of-ones-own-weave-your-own-web/', 'http://bavatuesdays.com/dtlt-today-episode-104-umws-domain-of-ones-own/', 'http://bavatuesdays.com/y-u-no-domain-of-ones-own/', 'http://bavatuesdays.com/a-domain-of-ones-own-to-community-syndication-hubs/', 'http://bavatuesdays.com/domain-of-ones-own-faculty-initiative/', 'http://bavatuesdays.com/domain-of-ones-own-discussion-on-chronicles-tech-therapy/', 'http://bavatuesdays.com/a-domain-of-ones-own-elevator-pitch/', 'http://bavatuesdays.com/a-domain-of-ones-own-and-the-realism-of-the-web/', 'http://bavatuesdays.com/domain-of-ones-own-has-been-funded/', 'http://bavatuesdays.com/domain-of-ones-own-as-educational-pilot-of-federated-web/', 'http://bavatuesdays.com/got-my-head-in-the-cloud-udell-on-domain-of-ones-own/', 'http://bavatuesdays.com/domain-of-ones-own-as-legacy-archival-project/', 'http://bavatuesdays.com/masters-of-our-domain-names-umw-to-pilot-domain-of-ones-own/', 'http://bavatuesdays.com/coventry-domains/', 'http://bavatuesdays.com/domains-of-online-scholarly-presence/', 'http://bavatuesdays.com/georgetown-slavery-site/', 'http://bavatuesdays.com/putting-domains-infrastructure-in-the-cloud/', 'http://bavatuesdays.com/changing-account-domains-in-whm/', 'http://bavatuesdays.com/domains-as-ground-zero-for-the-struggle-of-agency/', 'http://bavatuesdays.com/reclaiming-community-at-byu-with-known/', 'http://bavatuesdays.com/digital-pedagogy-empowered-choice-and-personal-domains/', 'http://bavatuesdays.com/sleazy-design-or-the-ugly-world-of-web-hosting-and-domain-registrars/', 'http://bavatuesdays.com/domains-and-the-cost-of-innovation/', 'http://bavatuesdays.com/api-domains-summit/', 'http://bavatuesdays.com/domain-knowledge/', 'http://bavatuesdays.com/an-art-portfolio-of-ones-own/', 'http://bavatuesdays.com/umw-domains-data-through-spring-2015/', 'http://bavatuesdays.com/scaling-domains/', 'http://bavatuesdays.com/umw-domains-is-not-radical/', 'http://bavatuesdays.com/indie-web-domains/', 'http://bavatuesdays.com/becoming-well-known/', 'http://bavatuesdays.com/connected-courses-its-time-to-reclaim-your-domain/', 'http://bavatuesdays.com/visions-of-known/', 'http://bavatuesdays.com/15550/', 'http://bavatuesdays.com/teaching-without-wordpress-exploring-the-known-world/', 'http://bavatuesdays.com/umw-domains-vs-umw-blogs/', 'http://bavatuesdays.com/eight-new-things-that-rule-about-umw-domains/', 'http://bavatuesdays.com/talking-domains-all-semester-long/', 'http://bavatuesdays.com/the-many-faces-of-domain/', 'http://bavatuesdays.com/domains-in-stop-motion/', 'http://bavatuesdays.com/umw-domains-now-with-more-community/', 'http://bavatuesdays.com/domains-in-the-afterglow/', 'http://bavatuesdays.com/what-richard-scarry-has-to-teach-us-about-domains/', 'http://bavatuesdays.com/master-of-my-domain/', 'http://bavatuesdays.com/rainbow-dash-on-umw-domains/', 'http://bavatuesdays.com/umw-domains-goes-back-to-school/', 'http://bavatuesdays.com/talking-domains-at-dml2014/', 'http://bavatuesdays.com/umw-domains-a-win-for-open/', 'http://bavatuesdays.com/davidson-domains/', 'http://bavatuesdays.com/course-domains/', 'http://bavatuesdays.com/dtlt-today-episode-107-marie-mcallisters-domain-of-her-own/', 'http://bavatuesdays.com/will-shuttleworth-reclaim-your-domain/', 'http://bavatuesdays.com/a-place-of-ones-own/', 'http://bavatuesdays.com/reclaim-your-domain-honing-the-vision/', 'http://bavatuesdays.com/the-domain-is-right/', 'http://bavatuesdays.com/reclaim-hosting-battling-digital-somnabulism-one-domain-at-a-time/', 'http://bavatuesdays.com/open-dialogue-domains-of-ones-own/', 'http://bavatuesdays.com/hardboiled-domains-6wordstory-and-hemingway/', 'http://bavatuesdays.com/ds106-week-1-introductions-webhosts-and-domain-of-your-own/', 'http://bavatuesdays.com/summer-of-love-domain-mapping/', 'http://bavatuesdays.com/an-integrated-domain/', 'http://bavatuesdays.com/the-overselling-of-open/', 'http://bavatuesdays.com/opening-pandoras-box-at-coventry/', 'http://bavatuesdays.com/fits-digital-spa/', 'http://bavatuesdays.com/changing-storage-quota-for-cpanel-accounts/', 'http://bavatuesdays.com/the-reclaiming-innovation-roadshow-at-coventry-university/', 'http://bavatuesdays.com/now-in-stereo/', 'http://bavatuesdays.com/the-personal-in-indie/', 'http://bavatuesdays.com/six-months-an-apprentice/', 'http://bavatuesdays.com/this-is-why-we-cant-have-nice-things-in-virginia-edtech/', 'http://bavatuesdays.com/small-systems-integration/', 'http://bavatuesdays.com/reclaim-your-hypothesis/', 'http://bavatuesdays.com/coffee-and-ds106-at-fredxchange/', 'http://bavatuesdays.com/six-years-of-stats-on-umw-blogs/', 'http://bavatuesdays.com/reclaim-the-portfolio/', 'http://bavatuesdays.com/10000-and-1-reclaimers/', 'http://bavatuesdays.com/what-has-wordpress-ever-done-for-us/', 'http://bavatuesdays.com/the-indie-edtech-movement/', 'http://bavatuesdays.com/initial-notes-on-an-api-driven-community-site-for-byu/', 'http://bavatuesdays.com/reclaiming-state-u/', 'http://bavatuesdays.com/re-ordering-pizza-in-2015/', 'http://bavatuesdays.com/a-decade-of-class-presentations/', 'http://bavatuesdays.com/a-long-short-history-of-reclaim-hosting/', 'http://bavatuesdays.com/single-most-important-development-in-edtech-in-last-2-years/', 'http://bavatuesdays.com/two-years-of-reclaim-hosting/', 'http://bavatuesdays.com/dukes-website-has-gone-docker/', 'http://bavatuesdays.com/on-maelstroms-and-syndication-buses/', 'http://bavatuesdays.com/a-personal-api/', 'http://bavatuesdays.com/the-university-api-an-unconference/', 'http://bavatuesdays.com/the-reclaim-code/', 'http://bavatuesdays.com/independent-teaching-networks/', 'http://bavatuesdays.com/dtlts-hurley-award-winner-martha-burtis/', 'http://bavatuesdays.com/password-management-ground-zero-for-digital-literacy/', 'http://bavatuesdays.com/how-automobiles-super-highways-and-containerization-helped-me-understand-the-future-of-the-web/', 'http://bavatuesdays.com/a-university-api/', 'http://bavatuesdays.com/the-wire-come-to-life/', 'http://bavatuesdays.com/reclaim-the-web-with-reclaim-hosting/', 'http://bavatuesdays.com/diverse-literacies-and-thinking-like-the-web/', 'http://bavatuesdays.com/catching-up-with-reclaim-hosting/', 'http://bavatuesdays.com/digital-agency-in-the-21st-century/', 'http://bavatuesdays.com/blogging-from-behind/', 'http://bavatuesdays.com/openva-2-0-october-18th-2014/', 'http://bavatuesdays.com/im-a-reclaimer-now/', 'http://bavatuesdays.com/connected-courses/', 'http://bavatuesdays.com/the-stump-speech-for-higher-eds-relevance-that-wasnt/', 'http://bavatuesdays.com/a-new-wave-of-open/', 'http://bavatuesdays.com/where-reclaims-going/', 'http://bavatuesdays.com/tic104-how-it-works-guide/', 'http://bavatuesdays.com/reclaiming-innovation/', 'http://bavatuesdays.com/lost-in-the-stacks/', 'http://bavatuesdays.com/has-the-time-arrived-for-hosted-lifebits/', 'http://bavatuesdays.com/a-problem-of-coherence/', 'http://bavatuesdays.com/hitchcock-motifs/', 'http://bavatuesdays.com/cyborg-tactic/', 'http://bavatuesdays.com/post-conference-sloan-c-interview/', 'http://bavatuesdays.com/playing-host-to-higher-eds-long-overdue-web-party/', 'http://bavatuesdays.com/trojan-horses-in-the-afterglow-at-sloan-c/', 'http://bavatuesdays.com/egypt-calling-or-why-open-rules/', 'http://bavatuesdays.com/humans-in-the-afterglow/', 'http://bavatuesdays.com/re-routing-cyberinfrastructures/', 'http://bavatuesdays.com/reclaim-the-handout/', 'http://bavatuesdays.com/teaching-technology-in-the-afterglow-at-baruch-college/', 'http://bavatuesdays.com/virtualization/', 'http://bavatuesdays.com/tilde-as-approximation/', 'http://bavatuesdays.com/dtlt-today-episode-111-jon-pinedas-open-doors/', 'http://bavatuesdays.com/devouring-videos/', 'http://bavatuesdays.com/when-user-was-equal-to-developer/', 'http://bavatuesdays.com/how-the-web-was-ghettoized-for-teaching-and-learning-in-higher-ed/', 'http://bavatuesdays.com/classes-i-want-to-teach/', 'http://bavatuesdays.com/analog-futures/', 'http://bavatuesdays.com/a-study-in-ds106/', 'http://bavatuesdays.com/digital-scholars-institute/', 'http://bavatuesdays.com/technical-vistas-flat-files-and-apis/', 'http://bavatuesdays.com/student-coded-projects-for-dtlt/', 'http://bavatuesdays.com/reclaim-workshop/', 'http://bavatuesdays.com/reading-capital-a-long-overdue-postmortem/', 'http://bavatuesdays.com/tiny-tiny-rss/', 'http://bavatuesdays.com/andrea-livi-smith-teaches-learns-and-lives-by-design/', 'http://bavatuesdays.com/de-icing-the-mooc-research-conference/', 'http://bavatuesdays.com/shuttleworth-flash-grant-update/', 'http://bavatuesdays.com/open-public-educational-publishing-platforms-4life/', 'http://bavatuesdays.com/where-have-the-online-neighborhoods-gone/', 'http://bavatuesdays.com/reclaim-the-chronicle/', 'http://bavatuesdays.com/decentering-syndication-or-a-push-away-from-rss/', 'http://bavatuesdays.com/what-im-up-to/', 'http://bavatuesdays.com/wrigley-ivy-jack-bales-on-the-chicago-cubs/', 'http://bavatuesdays.com/syndicated-personal-portfolios-the-case-of-stephen-j-farnsworth/', 'http://bavatuesdays.com/building-with-howard-creating-an-open-source-learning-environment-pt-2/', 'http://bavatuesdays.com/reclaim-hosting-is-live/', 'http://bavatuesdays.com/welcome-to-cloud-city/', 'http://bavatuesdays.com/syndicate-this-a-practical-dream-vision-of-syndication-for-umws-website/', 'http://bavatuesdays.com/paris-is-burning-through-syndication/', 'http://bavatuesdays.com/an-ode-to-umw-faculty/', 'http://bavatuesdays.com/golou-or-public-scholarship-in-the-digital-age/', 'http://bavatuesdays.com/syndication-oriented-architecture-a-solution-to-problem-of-coherence/', 'http://bavatuesdays.com/umws-innovation-isnt-technical-its-narrative/', 'http://bavatuesdays.com/osus-writers-talk-platforms-that-unlock-passion/', 'http://bavatuesdays.com/reclaim-open-learning/', 'http://bavatuesdays.com/the-awareness-network-the-web-as-context-engine/', 'http://bavatuesdays.com/ryan-brazell-joining-umws-dtlt-in-july/', 'http://bavatuesdays.com/can-universities-reclaim-the-web-too/', 'http://bavatuesdays.com/it-takes-a-liberal-arts-village-to-raise-a-digital-campus/', 'http://bavatuesdays.com/rambo-kills/', 'http://bavatuesdays.com/digital-networked-open/', 'http://bavatuesdays.com/fall-2012-report-card-for-dtlt/', 'http://bavatuesdays.com/nothing-is-lost/', 'http://bavatuesdays.com/7-years-later/', 'http://bavatuesdays.com/tales-from-the-teaching-crypt-education-after-online/', 'http://bavatuesdays.com/edstartup-meets-the-bava/', 'http://bavatuesdays.com/a-culture-of-innovation/', 'http://bavatuesdays.com/open-architecture-a-vision-beyond-the-massive-hype/', 'http://bavatuesdays.com/hardboiled-blogging-and-the-art-of-communicating/', 'http://bavatuesdays.com/the-roach-motel/', 'http://bavatuesdays.com/designing-a-hardboiled-course-site/', 'http://bavatuesdays.com/the-state-of-aggregation-at-umw/', 'http://bavatuesdays.com/a-round-up-of-fall-2012-projects-at-dtlt/', 'http://bavatuesdays.com/from-the-archive-els-blogs/', 'http://bavatuesdays.com/refocusing-and-refueling-keene-caulfield-and-udell/', 'http://bavatuesdays.com/umws-website-poised-to-become-syndication-hub-and-by-extension-relevant/', 'http://bavatuesdays.com/umw-blogs-a-k-a-old-faithful/', 'http://bavatuesdays.com/networks-within-networks-humans-technologies-and-metaphors/', 'http://bavatuesdays.com/faculty-academy-2012-under-disruption/', 'http://bavatuesdays.com/umw-featured-in-elis-7-things-about-new-learning-ecosystems/', 'http://bavatuesdays.com/innovation-as-a-communal-act/', 'http://bavatuesdays.com/you-know-what-dtlt-is-pretty-sick-right-now/', 'http://bavatuesdays.com/eduglu-revisited-the-syndication-bus-2012/', 'http://bavatuesdays.com/psu-4life/', 'http://bavatuesdays.com/20-examples-from-umw-blogs-part-2/', 'http://bavatuesdays.com/digital-storytelling-week-2/', 'http://bavatuesdays.com/digital-storytelling-the-course/', 'http://bavatuesdays.com/duke-cit-presentation-do-you-believe-in-magic/', 'http://bavatuesdays.com/umw-blogs-featured-in-educauses-7-things-for-ples/', 'http://bavatuesdays.com/start-with-the-demo-magic-trick/', 'http://bavatuesdays.com/open-is-always-outward-facing/', 'http://bavatuesdays.com/mozilla-open-education-course/', 'http://bavatuesdays.com/oer16-in-conversation/', 'http://bavatuesdays.com/digital-dioramas/', 'http://bavatuesdays.com/the-view-from-here/', 'http://bavatuesdays.com/creating-a-reseller-account-in-cpanel/', 'http://bavatuesdays.com/caught-in-the-sandstorm/', 'http://bavatuesdays.com/personal-apis-and-academic-libraries/', 'http://bavatuesdays.com/digital-pedagogy-as-empowered-choice/', 'http://bavatuesdays.com/installing-wordpress-multisite-and-using-feedwordpress/', 'http://bavatuesdays.com/ds106-interview-for-reclaim-open-learning/', 'http://bavatuesdays.com/this-week-in-ds106-episode-1/', 'http://bavatuesdays.com/ds106-the-summer-of-oblivion/', 'http://bavatuesdays.com/innovation-in-elearning-interview/', 'http://bavatuesdays.com/the-ds106-99-1-rapid-prototyping-the-mashup/', 'http://bavatuesdays.com/ds106-an-internet-odyssey/', 'http://bavatuesdays.com/the-future-of-wpmu/', 'http://bavatuesdays.com/day-107-playskool-mcdonalds-set/', 'http://bavatuesdays.com/one-blogor-many-a-closer-look-at-american-technology-and-culture/', 'http://bavatuesdays.com/bavacon-or-how-blog-branding-ate-my-soul/', 'http://bavatuesdays.com/syndicatin-welfare-umw-blogs-syndication-framework-on-the-cheap/', 'http://bavatuesdays.com/the-last-american-pirate/', 'http://bavatuesdays.com/this-aint-yo-mamas-e-portfolio-part-2/', 'http://bavatuesdays.com/high-school-hell-cats/', 'http://bavatuesdays.com/importing-a-single-wp-blog-to-a-wpmu-installation/', 'http://bavatuesdays.com/how-open-source-is-sakai/', 'http://www.digitalpedagogylab.com/hybridped/maggies-digital-content-farm/',  'http://www.digitalpedagogylab.com/hybridped/making-breaking-rethinking-web-higher-ed/', 'http://umwdtlt.com/a-brief-history-of-domain-of-ones-own-part-1/', 'http://umwdtlt.com/whos-afraid-domain-ones/', 'http://umwdtlt.com/an-infographic-of-ones-own/', 'http://umwdtlt.com/clone-this-websiteintroducing-peasy/', 'http://umwdtlt.com/vision-and-change-at-umw/', 'http://umwdtlt.com/coding-serendipity-domain-ones/', 'http://umwdtlt.com/claiming-a-domain-of-my-own-overwhelmed-by-wordpress/', 'http://umwdtlt.com/claiming-a-domain-of-my-own/', 'http://peterorabaugh.org/domain-2/domain-of-ones-own-research/']

database = []

for url_to_scrape in url_list:
    post = requests.get(url_to_scrape)
    #print(post.text) # for debugging
    soup = BeautifulSoup(post.text, 'lxml')

    ## find page content

    if soup.find('div', class_='entry-content') and soup.find('div', class_='entry-content') != None:
        page_data = soup.find('div', class_='entry-content') # WordPress 1
    elif soup.find('div', class_='single-entry-content') and soup.find('div', class_='single-entry-content') != None:
        page_data = soup.find('div', class_='single-entry-content') # WordPress 1a
    elif soup.find('div', class_='post-content') and soup.find('div', class_='post-content') != None:
        page_data = soup.find('div', class_='post-content') # WordPress 2
    elif soup.find('div', class_='gdlr-blog-content') and soup.find('div', class_='gdlr-blog-content') != None:
        page_data = soup.find('div', class_='gdlr-blog-content') # WordPress 3 (Hybrid Pedagogy)
    elif soup.find('div', class_='entry-body') and soup.find('div', class_='entry-body') != None:
        page_data = soup.find('div', class_='entry-body') # WordPress 4
    elif soup.find('div', class_='post-content inner') and soup.find('div', class_='post-content inner') != None:
        page_data = soup.find('div', class_='post-content inner') # Ghost
    elif soup.find('div', class_='blog__content') and soup.find('div', class_='blog__content') != None:
        page_data = soup.find('div', class_='blog__content') # ProfHacker
    elif soup.find('section', class_='post-content') and soup.find('section', class_='post-content') != None:
        page_data = soup.find('section', class_='post-content') # Hack Education
    elif soup.find('div', class_='field-item even') and soup.find('div', class_='field-item even') != None:
        page_data = soup.find('div', class_='field-item even') # IHE
    elif soup.find('div', class_='entry__content') and soup.find('div', class_='entry__content') != None:
        page_data = soup.find('div', class_='entry__content') # HuffPo
    elif soup.find('main', class_='postArticle-content') and soup.find('main', class_='postArticle-content') != None:
        page_data = soup.find('main', class_='postArticle-content') # Medium
    elif soup.find('div', class_='textblock--post') and soup.find('div', class_='textblock--post') != None:
        page_data = soup.find('div', class_='textblock--post') # Medium
    elif soup.find('div', class_='post_body') and soup.find('div', class_='post_body') != None:
        page_data = soup.find('div', class_='post_body') # gRSShopper
    elif soup.find('div', class_='article__content') and soup.find('div', class_='article__content') != None:
        page_data = soup.find('div', class_='article__content') # IHE
    elif soup.find('div', class_='article--content') and soup.find('div', class_='article--content') != None:
        page_data = soup.find('div', class_='article--content') # Blue Review
    elif soup.find('article', class_='content') and soup.find('article', class_='content') != None:
        page_data = soup.find('article', class_='content') # Wired
    elif soup.find('div', class_='content') and soup.find('div', class_='content') != None:
        page_data = soup.find('div', class_='content') # Getting Smart
    elif soup.find('section', class_='userMarkup') and soup.find('section', class_='userMarkup') != None:
        page_data = soup.find('section', class_='userMarkup').contents[1] # Davidson
    elif soup.find('div', class_='left-content') and soup.find('div', class_='left-content') != None:
        page_data = soup.find('div', class_='left-content') # MSU
    else:
        page_data = 'none'
    try:
        post_content_to_write = str(page_data).encode(sys.stdout.encoding, errors='replace')
    except:
        post_content_to_write = 'none'

    ## get page author
    ## Educause authors will have to be added manually
    ## Medium authors will have to be added manually

    if soup.find('span', class_="author") and soup.find('span', class_="author") != None:
        try:
            author = soup.find('span', class_="author").span.a.string # WordPress 1a
        except:
            try:
                author = soup.find('span', class_="author").a.string # Davidson
            except:
                author = soup.find('span', class_="author").string # WordPress 1b
    elif soup.find('a', class_="author") and soup.find('a', class_="author") != None:
        try:
            author = soup.find('a', class_="author").span.string # WordPress 2
        except:
            author = soup.find('a', class_="author").string # WordPress 2
    elif soup.find('span', class_="byline") and soup.find('span', class_="byline") != None:
        try:
            author = soup.find('span', class_="byline").a.string # WordPress 3
        except:
            author = soup.find('span', class_="byline").string # WordPress 3
    elif soup.find('p', class_="post-author") and soup.find('p', class_="post-author") != None:
        author = soup.find('p', class_="post-author").a.string # WordPress 4
    elif soup.find('div', class_="entry-author-byline") and soup.find('div', class_="entry-author-byline") != None:
        author = soup.find('div', class_="entry-author-byline").a.string # WordPress 5
    elif soup.find('span', class_="entry-author") and soup.find('span', class_="entry-author") != None:
        author = soup.find('span', class_="entry-author").string.strip('by ') # WordPress 6
    elif soup.find('span', class_="post-meta") and soup.find('span', class_="post-meta") != None:
        author = soup.find('span', class_="post-meta").a.string # WordPress 7 (Pete Rorabaugh)
    elif soup.find('div', class_="blog__author") and soup.find('div', class_="blog__author") != None:
        author = soup.find('div', class_="blog__author").a.string # ProfHacker
    elif soup.find('h4', class_="author-name") and soup.find('h4', class_="author-name") != None:
        author = soup.find('h4', class_="author-name").string # Hack Education
    elif soup.find('span', class_="author-card__details__name") and soup.find('span', class_="author-card__details__name") != None:
        author = soup.find('span', class_="author-card__details__name").string # HuffPo
    elif soup.find('a', class_="username") and soup.find('a', class_="username") != None:
        author = soup.find('a', class_="username").string # IHE
    elif soup.find('span', class_="entry-author-name") and soup.find('span', class_="entry-author-name") != None:
        author = soup.find('span', class_="entry-author-name").string # Domain Name Wire
    elif soup.find('a', class_="profile-name-link") and soup.find('a', class_="profile-name-link") != None:
        author = soup.find('a', class_="profile-name-link").string # BlogSpot
    elif soup.find('span', class_="post_author") and soup.find('span', class_="post_author") != None:
        author = soup.find('span', class_="post_author").a.string # Tumblr
    elif soup.find('div', class_="post__header-secondary") and soup.find('div', class_="post__header-secondary") != None:
        author = soup.find('div', class_="post__header-secondary").contents[1].string # EdSurge
    else:
        author = 'none'

    ## get page date
    ## IHE dates will have to be added manually
    ## Hybrid Pedagogy dates will have to be added manually
    ## Medium dates will have to be added manually

    if soup.find('span', class_="entry-date") and soup.find('span', class_="entry-date") != None:
        page_date = soup.find('span', class_="entry-date").string # WordPress 1
    elif soup.find('time', class_="entry-date") and soup.find('time', class_="entry-date") != None:
        page_date = soup.find('time', class_="entry-date").string # WordPress 2
    elif soup.find('div', class_="date-info") and soup.find('div', class_="date-info") != None:
        temp_date = soup.find('div', class_="date-info").string # WordPress Uncode DTLT blog
        page_date = datetime.datetime.strptime(temp_date, '%B %d, %Y').strftime('%Y-%m-%d')
    elif soup.find('time') and soup.find('time') != None:
        temp_date = soup.find('time').string
        try:
            page_date = datetime.datetime.strptime(temp_date, '%d %b %Y').strftime('%Y-%m-%d') # Hack Education
        except:
            page_date = temp_date.strip() # Davidson
    elif soup.find('span', class_="date") and soup.find('span', class_="date") != None:
        try:
            page_date = soup.find('span', class_="date").a.string # WordPress 3
        except:
            page_date = soup.find('span', class_="date").string # WordPress 3
    elif soup.find('p', class_="post-date") and soup.find('p', class_="post-date") != None:
        page_date = soup.find('p', class_="post-date").a.string # WordPress 4
    elif soup.find('span', class_="postday") and soup.find('span', class_="postday") != None:
        try:
            page_date = soup.find('span', class_="postday").a.string # WordPress 5
        except:
            page_date = soup.find('span', class_="postday").string # WordPress 5
    elif soup.find('span', class_="post-meta") and soup.find('span', class_="post-meta") != None:
        page_date = soup.find('span', class_="post-meta").contents[3].string # WordPress 6
    elif soup.find('div', class_="blog__author") and soup.find('div', class_="blog__author") != None:
        page_date = soup.find('div', class_="blog__author").time.string # ProfHacker
    elif soup.find('div', class_="timestamp") and soup.find('div', class_="timestamp") != None:
        temp_date = soup.find('div', class_="timestamp").span.string # HuffPo
        page_date = datetime.datetime.strptime(temp_date.split(' ')[0], '%m/%d/%Y').strftime('%Y-%m-%d')
    elif soup.find('h2', class_="date-header") and soup.find('h2', class_="date-header") != None:
        start_date = soup.find('h2', class_="date-header").string.strip() # BlogSpot
        temp_date = start_date.split(', ')[1] + ', ' + start_date.split(', ')[2]
        page_date = datetime.datetime.strptime(temp_date, '%B %d, %Y').strftime('%Y-%m-%d')
    elif soup.find('span', class_="byline") and soup.find('span', class_="byline") != None:
        start_date = soup.find('span', class_="byline").abbr.string.strip() # Education Week
        temp_date = start_date.split(' ')[0] + ' ' + start_date.split(' ')[1] + ' ' + start_date.split(' ')[2]
        page_date = datetime.datetime.strptime(temp_date, '%B %d, %Y').strftime('%Y-%m-%d')
    elif soup.find('span', class_="article--date") and soup.find('span', class_="article--date") != None:
        temp_date = soup.find('span', class_="article--date").string # Blue Review
        page_date = datetime.datetime.strptime(temp_date, '%m.%d.%Y').strftime('%Y-%m-%d')
    elif soup.find('div', class_="post__header-secondary") and soup.find('div', class_="post__header-secondary") != None:
        temp_date = soup.find('div', class_="post__header-secondary").contents[3].string # EdSurge
        page_date = datetime.datetime.strptime(temp_date, '%b %d, %Y').strftime('%Y-%m-%d')
    elif soup.find('div', class_="by-author-date") and soup.find('div', class_="by-author-date") != None:
        temp_date = soup.find('div', class_="by-author-date").string.strip() # Tumblr
        page_date = datetime.datetime.strptime(temp_date, '%B %d, %Y').strftime('%Y-%m-%d')
    #elif soup.find('div', class_="notes") and soup.find('div', class_="notes") != None:
    #    temp_date = soup.find('div', class_="notes").contents[6].string # Tumblr
    #    page_date = datetime.datetime.strptime(temp_date, '%b. %d, %Y').strftime('%Y-%m-%d')
    else:
        page_date = 'none'
    try:
        formatted_date = datetime.datetime.strptime(page_date, '%B %d, %Y').strftime('%Y-%m-%d')
    except:
        formatted_date = page_date

    ## get page title

    if soup.find('h1', class_="entry-title") and soup.find('h1', class_="entry-title") != None:
        title = soup.find('h1', class_="entry-title").string # WordPress
    elif soup.find('h1', class_="headline__title") and soup.find('h1', class_="headline__title") != None:
        title = soup.find('h1', class_="headline__title").string # HuffPo
    elif soup.find('title') and soup.find('title') != 'None':
        title = soup.find('title').string.strip().split(' | ')[0].split(' – ')[0].split(' - ')[0] # General
    elif soup.find('h1') and soup.find('h1') != None:
        title = soup.find('h1').string # IHE
    else:
        title = 'none'
    try:
        page_title = str(title).encode(sys.stdout.encoding, errors='replace').decode('utf-8')
    except:
        page_title = 'none'

    write_to_file('tempfile.txt', post_content_to_write)
    raw_text = subprocess.check_output(['python', 'html2text.py', 'tempfile.txt']).decode('utf-8')

    data_row = []
    data_row.append(author)
    data_row.append(page_title.strip())
    data_row.append(url_to_scrape)
    data_row.append(str(formatted_date))
    data_row.append(raw_text.replace('\n', ' ').replace('\t', ' ').replace('*', '').replace('_', ''))

    database.append(data_row)
    print(author, page_title.strip(), formatted_date, url_to_scrape)
    #print(raw_text)

write_csv(database, 'dooo_scraped.csv')
