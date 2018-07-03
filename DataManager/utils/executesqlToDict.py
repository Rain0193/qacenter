# coding:utf-8
from django.db import connection, transaction
from django.db import models
from django.db.models.fields.related import ManyToManyField

'''执行django原始sql语句  并返回一个数组对象'''
def executeQuery(sql):
        cursor = connection.cursor()  # 获得一个游标(cursor)对象
        cursor.execute(sql)
        rawData = cursor.fetchall()
        print(rawData)
        col_names = [desc[0] for desc in cursor.description]
        print(col_names)

        result = []
        for row in rawData:
            objDict = {}
            # 把每一行的数据遍历出来放到Dict中
            for index, value in enumerate(row):
                print(index, col_names[index], value)
                objDict[col_names[index]] = value

            result.append(objDict)

        return result

class PrintableModel(models.Model):
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        abstract = True