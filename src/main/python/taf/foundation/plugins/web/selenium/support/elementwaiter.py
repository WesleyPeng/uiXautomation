# Copyright 2017 {Flair} WESLEY PENG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from taf.foundation.api.ui.web import Waiter


class ElementWaiter(Waiter):
    def __init__(
            self,
            waiter=None,
            timeout=30.0,
            poll_frequency=1.0
    ):
        super(ElementWaiter, self).__init__(waiter, timeout)

        self.poll_frequency = poll_frequency or 1.0

    def wait(self, timeout=None):
        """
        Waits until the asynchronous animation complete
        :param timeout: float in seconds
        :return:
        """
        self.timeout = float(timeout or self.timeout)
        self.poll_frequency = float(self.poll_frequency)

        xmlhttp_animation_script = \
            'return (window.xmlhttp.readyState==4 && ' \
            'window.xmlhttp.status==200);'
        jquery_animation_script = 'return window.jQuery.active==0;'
        ajax_animation_script = 'return window.Ajax.activeRequestCount==0;'
        dojo_animation_script = \
            'return window.dojo.io.XMLHTTPTransport.inFlight.length==0;'
        angular_animation_script = \
            'return window.angular.element(document.body)' \
            '.injector().get("$http").pendingRequests.length==0;'

        animation_type_script_pairs = {
            'xmlhttp': xmlhttp_animation_script,
            'jQuery': jquery_animation_script,
            'Ajax': ajax_animation_script,
            'dojo': dojo_animation_script,
            'angular': angular_animation_script
        }

        for animation, script in animation_type_script_pairs.iteritems():
            ret = self.waiter.execute_script(
                'if (window.{}) return true; else return false;'.format(
                    animation
                )
            )

            ret = ret and ret != 'false'

            if ret:
                try:
                    WebDriverWait(
                        self.waiter,
                        self.timeout,
                        self.poll_frequency
                    ).until(
                        lambda driver: driver.execute_script(script),
                        'Failed to wait for loading '
                        '{} element in {} seconds'.format(
                            animation,
                            self.timeout
                        )
                    )
                except TimeoutException:
                    raise
