#
# # 重写io断开处理
# from socketio import Server
# from jsonpath import jsonpath
#
# def io_disconnect(user_id,sid):
#     with app.app_context():
#         user_target=User.query.filter(User.id==user_id).first()
#         sid_list=cache.get(str(user_id))
#         try:
#             sid_list.remove(sid)
#         except Exception as e:
#             print('user_id:{} sid:{}'.format(user_id,sid))
#             print('disconnect error!!!!',str(e))
#         if len(sid_list)==0:
#             cache.delete(str(user_id))
#             # user_target.is_online = False
#             db.session.commit()
#         else:
#             cache.set(str(user_id),sid_list)
#
#
# def _handle_eio_disconnect(self, sid):
#     """Handle Engine.IO disconnect event."""
#     try:
#         # print(self.environ)
#         # user_id=jsonpath(self.environ,'$.._user_id')
#         user_id=jsonpath(self.environ,'$..user_id')
#         _user_id=jsonpath(self.environ,'$.._user_id')
#         print('------->disconnecting<-------',user_id,_user_id)
#         if user_id:
#             print(jsonpath(self.environ,'$.._user_id',result_type='IPATH'))
#             user_id=user_id[0]
#             io_disconnect(user_id,sid)
#         else:
#             print(self.environ)
#     except Exception as e:
#         print('------------->error',str(e),'<------------')
#     self._handle_disconnect(sid, '/')
#     if sid in self.environ:
#         del self.environ[sid]
# Server._handle_eio_disconnect=_handle_eio_disconnect
