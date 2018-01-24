import abc

class NotificatorTemplate(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def send_message(self, msg):
		raise NotImplementedError()