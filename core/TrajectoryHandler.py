# -*- coding: utf-8 -*-

#    Copyright (C) 2013
#    by Klemens Fritzsche, pyplane@leckstrom.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Klemens Fritzsche'

import numpy as np
import pylab as pl
from scipy import integrate

#from core.canvas import MyMplCanvas
from core.Logging import myLogger
from core.ConfigHandler import myConfig
from core.System import mySystem


class TrajectoryHandler(object):
    def __init__(self):
        # dictionary for trajectories: first value is the initial condition,
        # the second value contains the matplotlib-data (y(x),x(t) and y(t)) as a stack list)

        self.traj_dict = {}

    def register_graph(self, parent, plot_pp, plot_x, plot_y):
        self.parent = parent
        self.plot_pp = plot_pp
        self.plot_x = plot_x
        self.plot_y = plot_y

    def clear_stack(self):
        self.traj_dict = {}

    def plot_trajectory(self, initial_condition, forward=None, backward=None):
        """
            This function plots the solution of the differential equation
            depending on the initial condition.

            In general, the trajectory consists of three elements:
            the forward trajectory, the backward trajectory and the marker for
            the initial condition, while each element can be turned off in the
            config file / settings tab.
            The elements are stored in a list. A dictionary stores this data
            with the initalCondition as its key, and the list as the value.

            Input variables:    - initialCondition (list with x and y
                                    coordinate)

            Return variables:   - none
        """
        if not forward and not backward:
            myLogger.warn_message("Please select forward and/or backward integration!")
            return False

        else:
            traj_stack = []

            traj_integrationtime = float(myConfig.read("Trajectories", "traj_integrationtime"))
            traj_integrationstep = float(myConfig.read("Trajectories", "traj_integrationstep"))
            time = pl.arange(0, traj_integrationtime, traj_integrationstep)

            if forward:
                # while integrate.ode.successful():
                # self.mySystem.jacobian(initialCondition)

                assert isinstance(initial_condition, list)
                self.x = integrate.odeint(mySystem.rhs, initial_condition, time)
                                          #, full_output=1, printmessg=1,       mxstep=20000)

                xvalue = self.x[:, 0]  # extract the x vector
                yvalue = self.x[:, 1]  # extract the dx/dt vector

                # masking xvalue (deleting invalid entries)
                #                 xvalue = np.ma.masked_outside(xvalue,-1*self.mySystem.max_norm,
                #                                               self.mySystem.max_norm)
                #                 myMask = xvalue.mask
                #                 new_time = np.ma.array(self.t, mask=myMask).compressed()
                #                 yvalue = np.ma.array(yvalue, mask=myMask).compressed()
                #                 xvalue = xvalue.compressed()
                #                 QtCore.pyqtRemoveInputHook()
                #                 embed()
                # masking yvalue
                #                 yvalue = np.ma.masked_outside(yvalue,-1*self.mySystem.max_norm,
                #                                               self.mySystem.max_norm)
                #                 myMask = yvalue.mask
                #                 new_time = np.ma.array(self.t, mask=myMask).compressed()
                #                 xvalue = np.ma.array(xvalue, mask=myMask)
                #                 yvalue = yvalue.compressed()

                #                 QtCore.pyqtRemoveInputHook()
                #                 embed()
                # plot solution in phase plane:
                traj_ppForwardColor = myConfig.read("Trajectories", "traj_ppForwardColor")
                plot1 = self.plot_pp.axes.plot(xvalue, yvalue, traj_ppForwardColor)

                # numpy array with both x and y values in pairs
                # TODO: might be faster if xvalues or yvalues greater than self.mySystem.max_norm
                # are masked before calculating the norm

                xvalue, yvalue = self.filter_values(xvalue, yvalue)

                # THIS HAS BEEN COMMENTED
                #                 z = np.column_stack((xvalue,yvalue))
                #
                #                 # put norm of each pair in numpy array
                #                 normed_z = np.array([np.linalg.norm(v) for v in z])
                #
                #                 # masking
                #                 max_norm = self.mySystem.max_norm
                #                 masked_normed_z = np.ma.masked_greater(normed_z, max_norm)
                #                 myMask = masked_normed_z.mask
                #
                #                 # new xvalue and yvalue
                #                 xvalue = np.ma.array(xvalue, mask=myMask)
                #                 yvalue = np.ma.array(yvalue, mask=myMask)
                # UNTIL HERE!

                # plot solution in x(t):
                traj_x_tColor = myConfig.read("Trajectories", "traj_x_tColor")
                plot2 = self.plot_x.axes.plot(time, xvalue, color=traj_x_tColor)

                # plot solution in y(t):
                traj_y_tColor = myConfig.read("Trajectories", "traj_y_tColor")
                plot3 = self.plot_y.axes.plot(time, yvalue, color=traj_y_tColor)

                # self.myLogger.message("forward trajectory done for initial condition "+str(initialCondition))
                traj_stack.append(plot1)
                traj_stack.append(plot2)
                traj_stack.append(plot3)

            # backward in time --------------------------------------------
            if backward:
                self.x_bw = integrate.odeint(mySystem.n_rhs, initial_condition, time)
                #, full_output=1, printmessg=1)#, mxstep=5000)
                # self.x_bw, infodict2 = integrate.odeint(self.mySystem.n_rhs,
                # initialCondition, self.t)#, full_output=1, printmessg=1)#, mxstep=5000)

                xvalue_bw = self.x_bw[:, 0]
                yvalue_bw = self.x_bw[:, 1]

                #                 # masking xvalue_bw (deleting invalid entries)
                #                 xvalue_bw = np.ma.masked_outside(xvalue_bw,1*self.mySystem.max_norm,
                #                                                  self.mySystem.max_norm)
                #                 yvalue_bw = np.ma.array(yvalue_bw, mask=xvalue_bw.mask)
                #                 xvalue_bw = xvalue_bw.compressed()
                #
                #                 # masking yvalue_bw
                #                 yvalue_bw = np.ma.masked_outside(yvalue_bw,1*self.mySystem.max_norm,
                #                                                  self.mySystem.max_norm)
                #                 xvalue = np.ma.array(xvalue, mask=yvalue.mask)
                #                 yvalue_bw = yvalue_bw.compressed()

                #                 xvalue, yvalue = self.filter_values(xvalue,yvalue)

                # plot in phase plane:
                traj_ppBackwardColor = myConfig.read("Trajectories", "traj_ppBackwardColor")
                plot4 = self.plot_pp.axes.plot(xvalue_bw, yvalue_bw, color=traj_ppBackwardColor)

                traj_stack.append(plot4)

            #                self.myLogger.message("backward trajectory
            #                                       done for initial condition "+str(initialCondition))

            # mark init:
            if myConfig.get_boolean("Trajectories", "traj_plotInitPoint"):
                traj_initPointColor = myConfig.read("Trajectories", "traj_initPointColor")
                plot5 = self.plot_pp.axes.plot(initial_condition[0],
                                               initial_condition[1],
                                               '.',
                                               color=traj_initPointColor)
                traj_stack.append(plot5)

            if len(traj_stack) != 0:
                # mark init:
                self.traj_dict[str(initial_condition)] = traj_stack

            # update_all
            self.parent.update_all()
            # return True

    def filter_values(self, xvalue, yvalue):
        z = np.column_stack((xvalue, yvalue))

        # put norm of each pair in numpy array
        normed_z = np.array([np.linalg.norm(v) for v in z])

        # masking
        max_norm = mySystem.max_norm
        masked_normed_z = np.ma.masked_greater(normed_z, max_norm)
        myMask = masked_normed_z.mask

        # new xvalue and yvalue
        xvalue = np.ma.array(xvalue, mask=myMask)
        yvalue = np.ma.array(yvalue, mask=myMask)

        return xvalue, yvalue

    def create_trajectory(self):
        initial_condition = self.parent.read_init()
        forward, backward = self.parent.trajectory_direction()

        cond1 = initial_condition[0] is not None
        cond2 = initial_condition[1] is not None
        # check if trajectory with initial_condition exists already
        cond3 = not str(initial_condition) in self.traj_dict

        if cond1 and cond2 and cond3:
            self.plot_trajectory(initial_condition, forward, backward)
            myLogger.message("New initial condition: " + str(initial_condition[0]) + ", " + str(initial_condition[1]))
        #except:
        #    myLogger.error_message("Please check intial condition!")

    def remove(self, init):
        """ this function removes a single trajectory specified by its initial value. not implemented right now
        """
        pass

    def remove_all(self):
        """ this function removes every trajectory in y(x), x(t) and y(t)
        """
        for i in self.traj_dict:
            # i is the next key
            for j in xrange(0, len(self.traj_dict[i])):
                # j is a list element from the traj_stack
                try:
                    self.traj_dict[i].pop()[0].remove()
                except Exception as error:
                    myLogger.debug_message("Could not delete trajectory")
                    myLogger.debug_message(str(type(error)))
                    myLogger.debug_message(str(error))
        self.parent.update_all()

myTrajectories = TrajectoryHandler()