
from framework.data_profiler import profile_source_data


def test_source_data_profile():
    report = profile_source_data()

    assert report["total_records"] == 5
    assert report["unique_customer_ids"] == 5
    assert report["null_names"] == 0
    assert report["null_emails"] == 0
    assert report["null_amounts"] == 0
    assert report["minimum_amount"] == 12000.0
    assert report["maximum_amount"] == 25000.0
    assert report["average_amount"] == 18400.0
