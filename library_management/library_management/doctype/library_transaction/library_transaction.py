# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

# from __future__ import unicode_literals
# import frappe
# from frappe.model.document import Document

# class LibraryTransaction(Document):
# 	pass
# -*- coding: utf-8 -*-
# Copyright (c) 2020, Nikhil and contributors
# For license information, please see license.txt

# from __future__ import unicode_literals
# # import frappe
# from frappe.model.document import Document

# class LibraryTransaction(Document):
# 	pass
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
import datetime
from frappe.utils import format_date


class LibraryTransaction(Document):
    def validate(self):
        date1 = frappe.utils.nowdate()
        last_transaction = frappe.get_list("Library Transaction",
                                           fields=["transaction_type",
                                                   "transaction_date"],
                                           filters={
                                               "article": self.article,
                                               "transaction_date": ("<=", self.transaction_date),
                                               "name": ("!=", self.name)
                                           })

        if date1 < self.transaction_date:
            frappe.throw("Not valid!!")
        if self.transaction_type == "Issue":
            msg = _(
                "Article {0} {1} has not been recorded as returned since {2}")
            if last_transaction and last_transaction[0].transaction_type == "Issue":
                frappe.throw(msg.format(self.article, self.article_name,
                                        last_transaction[0].transaction_date))
        else:
            if not last_transaction or last_transaction[0].transaction_type != "Issue":
                frappe.throw(_("Cannot return article not issued"))
