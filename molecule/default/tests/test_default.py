import os
import pytest
import sys

import testinfra.utils.ansible_runner

DEFAULT_HOST = 'all'

runner = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE'])
testinfra_hosts = runner.get_hosts(DEFAULT_HOST)


@pytest.mark.parametrize("pkg", [
    'openssl',
])
def test_pkg(host, pkg):
    package = host.package(pkg)
    assert package.is_installed



@pytest.fixture
def testvars(host):
    variables = runner.run(
        DEFAULT_HOST,
        'testvars.yml'
    )
    print >> open('/tmp/ansible_vars', 'w'), variables



# 2048 as specified in testvars.yml
# should be great to get that dynamically
@pytest.mark.parametrize('file, content', [
    ('/etc/ssl/dhparam-2048.pem', '-----END DH PARAMETERS-----'),
])
def test_files(host, file, content):
    f = host.file(file)

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains(content)
