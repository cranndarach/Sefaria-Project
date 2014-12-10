import pytest

from sefaria.model import *
from sefaria.system.exceptions import InputError
from sefaria.utils.util import list_depth


def test_verse_chunk():
    chunks = [
        TextChunk(Ref("Daniel 2:3"), "en", "The Holy Scriptures: A New Translation (JPS 1917)"),
        TextChunk(Ref("Daniel 2:3"), "he", "Tanach with Nikkud"),
        TextChunk(Ref("Daniel 2:3"), "en"),
        TextChunk(Ref("Daniel 2:3"), "he")
    ]
    for c in chunks:
        assert isinstance(c.text, basestring)
        assert len(c.text)


def test_chapter_chunk():
    chunks = [
        TextChunk(Ref("Daniel 2"), "en", "The Holy Scriptures: A New Translation (JPS 1917)"),
        TextChunk(Ref("Daniel 2"), "he", "Tanach with Nikkud"),
        TextChunk(Ref("Daniel 2"), "en"),
        TextChunk(Ref("Daniel 2"), "he")
    ]
    for c in chunks:
        assert isinstance(c.text, list)
        assert len(c.text)

def test_depth_1_chunk():
    c = TextChunk(Ref("Hadran"), "he")
    assert isinstance(c.text, list)
    c = TextChunk(Ref("Hadran 3"), "he")
    assert isinstance(c.text, basestring)

def test_out_of_range_chunks():
    # test out of range where text has length
    with pytest.raises(InputError):
        TextChunk(Ref("Genesis 80"), "he")

    # and where text does not have length
    t = TextChunk(Ref("Meshech Hochma 66"))
    assert t.text == []

    t = TextChunk(Ref("Meshech Hochma 66.4"))
    assert t.text == ""


def test_range_chunk():
    chunks = [
        TextChunk(Ref("Daniel 2:3-5"), "en", "The Holy Scriptures: A New Translation (JPS 1917)"),
        TextChunk(Ref("Daniel 2:3-5"), "he", "Tanach with Nikkud"),
        TextChunk(Ref("Daniel 2:3-5"), "en"),
        TextChunk(Ref("Daniel 2:3-5"), "he"),
    ]

    for c in chunks:
        assert isinstance(c.text, list)
        assert len(c.text) == 3


def test_spanning_chunk():
    chunks = [
        TextChunk(Ref("Daniel 2:3-4:5"), "en", "The Holy Scriptures: A New Translation (JPS 1917)"),
        TextChunk(Ref("Daniel 2:3-4:5"), "he", "Tanach with Nikkud"),
        TextChunk(Ref("Daniel 2:3-4:5"), "en"),
        TextChunk(Ref("Daniel 2:3-4:5"), "he")
    ]

    for c in chunks:
        assert isinstance(c.text, list)
        assert isinstance(c.text[0], list)
        assert len(c.text) == 3
        assert len(c.text[2]) == 5


def test_commentary_chunks():
    verse = TextChunk(Ref("Rashi on Exodus 3:1"), lang="he")
    rang = TextChunk(Ref("Rashi on Exodus 3:1-10"), lang="he")
    span = TextChunk(Ref("Rashi on Exodus 3:1-4:10"), lang="he")
    assert verse.text == rang.text[0]
    assert verse.text == span.text[0][0]

    verse = TextChunk(Ref("Rashi on Exodus 4:10"), lang="he")
    rang = TextChunk(Ref("Rashi on Exodus 4:1-10"), lang="he")
    assert rang.text[-1] == verse.text
    assert span.text[-1][-1] == verse.text


def test_spanning_family():
    f = TextFamily(Ref("Daniel 2:3-4:5"), context=0)

    assert isinstance(f.text, list)
    assert isinstance(f.he, list)
    assert len(f.text) == 3
    assert len(f.text[2]) == 5
    assert len(f.he) == 3
    assert len(f.he[2]) == 5
    assert isinstance(f.commentary[0], list)

    f = TextFamily(Ref("Daniel 2:3-4:5"))  # context = 1
    assert isinstance(f.text, list)
    assert isinstance(f.he, list)
    assert len(f.text) == 3
    assert len(f.text[2]) == 34
    assert len(f.he) == 3
    assert len(f.he[2]) == 34
    assert isinstance(f.commentary[0], list)




def test_family_chapter_result_no_merge():
    families = [
        TextFamily(Ref("Midrash Tanchuma.1.2")),  # this is supposed to get a version with exactly 1 en and 1 he.  The data may change.
        TextFamily(Ref("Daniel 2")),
        TextFamily(Ref("Daniel 4"), lang="en", version="The Holy Scriptures: A New Translation (JPS 1917)"),
        TextFamily(Ref("Daniel 4"), lang="he", version="Tanach with Nikkud")
    ]

    for v in families:
        assert isinstance(v.text, list)
        assert isinstance(v.he, list)

        c = v.contents()
        for key in ["text", "ref", "he", "book", "commentary"]:  # todo: etc.
            assert key in c


def test_chapter_result_merge():
    v = TextFamily(Ref("Mishnah_Yoma.1"))

    assert isinstance(v.text, list)
    assert isinstance(v.he, list)
    c = v.contents()
    for key in ["text", "ref", "he", "book", "sources", "commentary"]:  # todo: etc.
        assert key in c


def test_validate():
    passing_refs = [
        Ref("Exodus"),
        Ref("Exodus 3"),
        Ref("Exodus 3:4"),
        Ref("Exodus 3-5"),
        Ref("Exodus 3:4-5:7"),
        Ref("Exodus 3:4-7"),
        Ref("Rashi on Exodus"),
        Ref("Rashi on Exodus 3"),
        Ref("Rashi on Exodus 3:2"),
        Ref("Rashi on Exodus 3-5"),
        Ref("Rashi on Exodus 3:2-5:7"),
        Ref("Rashi on Exodus 3:2-7"),
        Ref("Rashi on Exodus 3:2:1"),
        Ref("Rashi on Exodus 3:2:1-3"),
        Ref("Rashi on Exodus 3:2:1-3:5:1"),
        Ref("Shabbat 7a"),
        Ref("Shabbat 7a-8b"),
        Ref("Shabbat 7a:12"),
        Ref("Shabbat 7a:12-23"),
        Ref("Shabbat 7a:12-7b:3"),
        Ref("Rashi on Shabbat 7a"),
        Ref("Rashi on Shabbat 7a-8b"),
        Ref("Rashi on Shabbat 7a:12"),
        Ref("Rashi on Shabbat 7a:12-23"),
        Ref("Rashi on Shabbat 7a:12-7b:3")
    ]
    for ref in passing_refs:
        TextChunk(ref, lang="he")._validate()


def test_save():
    # Delete any old ghost
    vs = ["Hadran Test", "Pirkei Avot Test", "Rashi on Pirkei Avot Test"]
    for vt in vs:
        try:
            Version().load({"versionTitle": vt}).delete()
        except:
            pass

    # create new version, depth 1
    v = Version({
        "language": "en",
        "title": "Hadran",
        "versionSource": "http://foobar.com",
        "versionTitle": "Hadran Test",
        "chapter": []
    }).save()
    # write to blank version
    c = TextChunk(Ref("Hadran 3"), "en", "Hadran Test")
    c.text = "Here's a translation for the eras"
    c.save()

    # write beyond current extent
    c = TextChunk(Ref("Hadran 5"), "en", "Hadran Test")
    c.text = "Here's another translation for the eras"
    c.save()

    # write within current extent
    c = TextChunk(Ref("Hadran 4"), "en", "Hadran Test")
    c.text = "Here's yet another translation for the eras"
    c.save()

    # verify
    c = TextChunk(Ref("Hadran"), "en", "Hadran Test")
    assert c.text[2] == "Here's a translation for the eras"
    assert c.text[3] == "Here's yet another translation for the eras"
    assert c.text[4] == "Here's another translation for the eras"

    # delete version
    v.delete()

    # create new version, depth 2
    v = Version({
        "language": "en",
        "title": "Pirkei Avot",
        "versionSource": "http://foobar.com",
        "versionTitle": "Pirkei Avot Test",
        "chapter": []
    }).save()

    # write to new verse of new chapter
    c = TextChunk(Ref("Pirkei Avot 2:3"), "en", "Pirkei Avot Test")
    c.text = "Text for 2:3"
    c.save()

    # extend to new verse of later chapter
    c = TextChunk(Ref("Pirkei Avot 3:4"), "en", "Pirkei Avot Test")
    c.text = "Text for 3:4"
    c.save()

    # write new chapter beyond created range
    c = TextChunk(Ref("Pirkei Avot 5"), "en", "Pirkei Avot Test")
    c.text = ["Text for 5:1", "Text for 5:2", "Text for 5:3", "Text for 5:4"]
    c.save()

    # write new chapter within created range
    c = TextChunk(Ref("Pirkei Avot 4"), "en", "Pirkei Avot Test")
    c.text = ["Text for 4:1", "Text for 4:2", "Text for 4:3", "Text for 4:4"]
    c.save()

    # write within explicitly created chapter
    c = TextChunk(Ref("Pirkei Avot 3:5"), "en", "Pirkei Avot Test")
    c.text = "Text for 3:5"
    c.save()
    c = TextChunk(Ref("Pirkei Avot 3:3"), "en", "Pirkei Avot Test")
    c.text = "Text for 3:3"
    c.save()

    # write within implicitly created chapter
    c = TextChunk(Ref("Pirkei Avot 1:5"), "en", "Pirkei Avot Test")
    c.text = "Text for 1:5"
    c.save()

    # Rewrite
    c = TextChunk(Ref("Pirkei Avot 4:2"), "en", "Pirkei Avot Test")
    c.text = "New Text for 4:2"
    c.save()

    # verify
    c = TextChunk(Ref("Pirkei Avot"), "en", "Pirkei Avot Test")
    assert c.text == [
        ["", "", "", "", "Text for 1:5"],
        ["", "", "Text for 2:3"],
        ["", "", "Text for 3:3", "Text for 3:4", "Text for 3:5"],
        ["Text for 4:1", "New Text for 4:2", "Text for 4:3", "Text for 4:4"],
        ["Text for 5:1", "Text for 5:2", "Text for 5:3", "Text for 5:4"]
    ]

    v.delete()



    # create new version, depth 3 - commentary
    v = Version({
        "language": "en",
        "title": "Rashi on Pirkei Avot",
        "versionSource": "http://foobar.com",
        "versionTitle": "Rashi on Pirkei Avot Test",
        "chapter": []
    }).save()


    # write to new verse of new chapter
    c = TextChunk(Ref("Rashi on Pirkei Avot 2:3"), "en", "Rashi on Pirkei Avot Test")
    c.text = ["Text for 2:3:1", "Text for 2:3:2"]
    c.save()

    # extend to new verse of later chapter
    c = TextChunk(Ref("Rashi on Pirkei Avot 3:4:3"), "en", "Rashi on Pirkei Avot Test")
    c.text = "Text for 3:4:3"
    c.save()

    # write new chapter beyond created range
    c = TextChunk(Ref("Rashi on Pirkei Avot 5"), "en", "Rashi on Pirkei Avot Test")
    c.text = [["Text for 5:1:1"], ["Text for 5:2:1"], ["Text for 5:3:1","Text for 5:3:2"],["Text for 5:4:1"]]
    c.save()

    # write new chapter within created range
    c = TextChunk(Ref("Rashi on Pirkei Avot 4"), "en", "Rashi on Pirkei Avot Test")
    c.text = [["Text for 4:1:1", "Text for 4:1:2", "Text for 4:1:3", "Text for 4:1:4"]]
    c.save()

    # write within explicitly created chapter
    c = TextChunk(Ref("Rashi on Pirkei Avot 3:5:1"), "en", "Rashi on Pirkei Avot Test")
    c.text = "Text for 3:5:1"
    c.save()
    c = TextChunk(Ref("Rashi on Pirkei Avot 3:3:3"), "en", "Rashi on Pirkei Avot Test")
    c.text = "Text for 3:3:3"
    c.save()

    # write within implicitly created chapter
    c = TextChunk(Ref("Rashi on Pirkei Avot 1:5"), "en", "Rashi on Pirkei Avot Test")
    c.text = ["Text for 1:5", "Text for 1:5:2"]
    c.save()

    # Rewrite
    c = TextChunk(Ref("Rashi on Pirkei Avot 4:1:2"), "en", "Rashi on Pirkei Avot Test")
    c.text = "New Text for 4:1:2"
    c.save()

    # verify
    c = TextChunk(Ref("Rashi on Pirkei Avot"), "en", "Rashi on Pirkei Avot Test")
    assert c.text == [
        [[], [], [], [],["Text for 1:5", "Text for 1:5:2"]],
        [[], [], ["Text for 2:3:1", "Text for 2:3:2"]],
        [[], [], ["", "", "Text for 3:3:3"], ["", "", "Text for 3:4:3"], ["Text for 3:5:1"]],
        [["Text for 4:1:1", "New Text for 4:1:2", "Text for 4:1:3", "Text for 4:1:4"]],
        [["Text for 5:1:1"], ["Text for 5:2:1"], ["Text for 5:3:1","Text for 5:3:2"],["Text for 5:4:1"]]
    ]






    v.delete()

    # write