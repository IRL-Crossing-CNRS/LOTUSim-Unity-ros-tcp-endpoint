from queue import Empty

import pytest

from ros_tcp_endpoint.tcp_sender import LatestWinsQueue, is_event_topic


def test_newest_pending_message_of_a_topic_replaces_the_older_one():
    q = LatestWinsQueue()
    q.put_latest("poses", b"old")
    q.put_latest("poses", b"new")
    q.put_latest("wind", b"w")
    assert [q.get(timeout=0), q.get(timeout=0)] == [b"new", b"w"]
    with pytest.raises(Empty):
        q.get(timeout=0)


def test_other_items_stay_in_order():
    q = LatestWinsQueue()
    q.put(b"handshake")
    q.put_latest("poses", b"p")
    q.put(b"log")
    assert [q.get(timeout=0) for _ in range(3)] == [b"handshake", b"p", b"log"]


def test_a_topic_sent_again_after_a_get_is_queued_again():
    q = LatestWinsQueue()
    q.put_latest("poses", b"1")
    assert q.get(timeout=0) == b"1"
    q.put_latest("poses", b"2")
    assert q.get(timeout=0) == b"2"


def test_renderer_cmd_is_an_event_topic():
    assert is_event_topic("/energy/renderer_cmd")
    assert is_event_topic("/energy/renderer_cmd/")
    assert not is_event_topic("/energy/renderer_poses")
