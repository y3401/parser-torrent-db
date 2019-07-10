# Скрипт для парсинга XML-дампа БД RuTracker.org

Адаптировано для 2 и 3 версии Python'a

Сам скрипт, справочник форумов ("forums.csv") и распакованный файл дампа бэкапа БД (берется с https://rutracker.org/forum/viewtopic.php?t=5591249) переименовать по маске "backup.yyyymmdd*.xml" и поместить в один каталог. (Для тестирования можно использовать представленный тут небольшой файл "backup.20180722_test.xml")

После запуска скрипта sax_parser.py, в зависимости от выбранного пункта меню, в текущем каталоге создается папка с датой бэкапа (например, "./20180722") и в нем файлы в формате CSV, с записями, разбитыми по категориям, в соответствие со справочником forums, либо каталог DB с базами "torrents.db3" и "content.db3".

В начале рекомендуется прогнать исходный файл через пункт "0", чтобы выявить недостающие разделы форумов для добавления их в справочник "forums.csv", указав дополнительно категорию. к которой эти форумы должны относиться.

Если это предварительно не сделать, то, если в справочнике нет какого-то нового форума, то запись попадает в файл "category_0.csv", а в БД проставляется категория 0.

Зафиксировано время обработки дампа размером 18Гб на PC с процессором Intel i5, ОЗУ 16 Gb и HDD Seagate 4Tb:
*    в CSV 22:04 мин.
*    конвертация в 2 файла DB - 3:28:17.

UPDATE: 
1. После выбора в качестве принимающего результат обработки диска SSD, вермя обработки значительно сократилось.
2. Конвертацию в CSV лучше выполнять после создания файла "torrents.db" посредством запуска "export_in_CSV.py" - также значительно быстрее, чем превоначальный вариант
